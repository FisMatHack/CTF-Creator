import os
import argparse
import random
from google import genai
from config import VULN_LIST
from prompt import build_prompt
from llm import generate_lab
from packaging import package_project

def guided_mode():
    vuln_input = input("Vulnerability (e.g., 'SQLi', 'random', 'random-3'):\n>> ").strip()
    target_vuln = vuln_input
    if vuln_input.lower().startswith("random"):
        num = int(vuln_input.split("-")[1]) if "-" in vuln_input else 1
        target_vuln = " and ".join(random.sample(VULN_LIST, min(num, len(VULN_LIST))))

    project_name = input("Project folder name:\n>> ").strip() or "ai_lab"
    include_writeup = input("Generate Writeup? (y/n):\n>> ").strip().lower() == 'y'
    return target_vuln, project_name, include_writeup

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vuln")
    parser.add_argument("-n", "--name")
    parser.add_argument("-w", "--writeup", action="store_true")
    parser.add_argument("-g", "--guided", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[!] GEMINI_API_KEY environment variable not found. Please set it.")
        exit(1)

    client = genai.Client(api_key=api_key)
    
    if args.guided or not (args.vuln and args.name):
        target_vuln, project_name, include_writeup = guided_mode()
    else:
        target_vuln, project_name, include_writeup = args.vuln, args.name, args.writeup
        if target_vuln.lower().startswith("random"):
            num = int(target_vuln.split("-")[1]) if "-" in target_vuln else 1
            target_vuln = " and ".join(random.sample(VULN_LIST, min(num, len(VULN_LIST))))

    prompt_text = build_prompt(target_vuln, include_writeup)
    lab_data = generate_lab(client, prompt_text, include_writeup)
    package_project(lab_data, project_name)

if __name__ == "__main__":
    main()
