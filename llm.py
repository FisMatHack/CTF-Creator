import re
from google.genai import types

def parse_llm_response(text):
    data = {"app_files": [], "dockerfile": "", "docker_compose_yml": "", "writeup_md": ""}
    
    if not text:
        return data
        
    file_pattern = re.compile(r'==FILE:\s*(.+?)\s*==\s*\n(.*?)\s*==ENDFILE==', re.DOTALL)
    for match in file_pattern.finditer(text):
        filepath = match.group(1).strip()
        content = match.group(2).strip()
        if content.startswith("```"): content = content.split('\n', 1)[-1]
        if content.endswith("```"): content = content.rsplit('\n', 1)[0]
            
        if filepath.lower() == "dockerfile": data["dockerfile"] = content.strip()
        elif filepath.lower() == "docker-compose.yml": data["docker_compose_yml"] = content.strip()
        else: data["app_files"].append({"path": filepath, "content": content.strip()})
            
    writeup_pattern = re.compile(r'==WRITEUP==(.*?)(?:==ENDWRITEUP==|$)', re.DOTALL | re.IGNORECASE)
    writeup_match = writeup_pattern.search(text)
    if writeup_match:
        writeup_content = writeup_match.group(1).strip()
        if writeup_content.startswith("```"): writeup_content = writeup_content.split('\n', 1)[-1]
        if writeup_content.endswith("```"): writeup_content = writeup_content.rsplit('\n', 1)[0]
        data["writeup_md"] = writeup_content.strip()
        
    return data

def generate_lab(client, prompt_text, include_writeup):
    max_retries = 3
    for attempt in range(max_retries):
        print(f"[*] AI working on the code. Please wait...")
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_text,
                config=types.GenerateContentConfig(max_output_tokens=8192, temperature=0.4)
            )
            
            if not hasattr(response, 'text') or not response.text:
                print("[!] AI returned an empty response. Retrying...")
                continue
                
            data = parse_llm_response(response.text)
            is_valid_code = bool(data.get("app_files") and data.get("dockerfile") and data.get("docker_compose_yml"))
            
            if is_valid_code:
                if include_writeup:
                    print("[*] Code generated successfully! AI is now writing the Writeup...")
                    writeup_prompt = f"""
                    Act as a Senior Penetration Tester and CTF Solver. I have generated a vulnerable application with this exact source code:
                    
                    {response.text}
                    
                    Your task: Write a 100% ACCURATE Markdown writeup for THIS SPECIFIC CODE.
                    
                    CRITICAL RULES FOR THE WRITEUP:
                    1. CODE AUDIT: You MUST read the provided PHP/HTML code carefully. Check exactly how the inputs are handled.
                    2. NO HALLUCINATIONS: If the code has a specific filter or quirks, your Exploit Steps MUST explain how to bypass that exact filter. Do not provide a generic payload that will fail against this specific code.
                    3. PROOF OF CONCEPT: Provide the exact, working URL, payload, or script needed to retrieve the FLAG{{...}} based ON THE CODE PROVIDED.
                    
                    Wrap your ENTIRE response inside these exact tags:
                    ==WRITEUP==
                    # Lab Writeup
                    ## Context
                    ## Vulnerability Analysis (Explain exactly where the flaw is in the code provided)
                    ## Exploitation Steps (Exact payloads that work against this code)
                    ## Remediation
                    ==ENDWRITEUP==
                    """
                    try:
                        w_resp = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=writeup_prompt,
                            config=types.GenerateContentConfig(max_output_tokens=4000, temperature=0.4)
                        )
                        w_data = parse_llm_response(w_resp.text)
                        if w_data.get("writeup_md"):
                            data["writeup_md"] = w_data["writeup_md"]
                            print("[+] Writeup generated!")
                        else:
                            print("[!] Warning: Writeup generation failed or was empty. Saving lab without it.")
                    except Exception as we:
                        print(f"[!] Warning: Could not generate writeup separately ({we}). Saving lab without it.")
                        
                return data
            else:
                print("[!] Warning: AI generated incomplete code. Retrying...")
        except Exception as e:
            print(f"[!] Connection or processing error: {e}")
            
    print("[!] Fatal Error: Could not generate a valid lab after 3 attempts.")
    exit(1)
