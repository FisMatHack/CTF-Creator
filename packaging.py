import os
import re
import shutil

def package_project(data, base_name):
    dir_temp = f"lab_{base_name.replace(' ', '_').lower()}"
    os.makedirs(os.path.join(dir_temp, "src"), exist_ok=True)
    
    for file_obj in data.get("app_files", []):
        path = file_obj["path"]
        content = file_obj["content"]
        if not path.startswith("src/") and path.lower().endswith(('.php', '.html', '.css', '.js', '.ts', '.jsx')):
            path = f"src/{path}"
            
        if path.endswith(".sh"):
            content = re.sub(r'while\s+.*?(?:do).*?sleep.*?(?:done)', '\n', content, flags=re.DOTALL | re.IGNORECASE)
            
            if "entrypoint" in path.lower() or "init" in path.lower():
                if "apache2-foreground" not in content and 'exec "$@"' not in content:
                    content += "\n\nexec apache2-foreground\n"
                
        full_path = os.path.join(dir_temp, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
            
    if data.get("dockerfile"):
        dockerfile_lines = data["dockerfile"].split('\n')
        sanitized_lines = []
        has_chmod = False
        
        for line in dockerfile_lines:
            stripped_line = line.strip()
            
            if "apt-get" in stripped_line and ("mysqli" in stripped_line or "pdo" in stripped_line):
                line = re.sub(r'\b(mysqli|pdo|pdo_mysql)\b', '', line)
                
            if "chmod" in stripped_line and ".sh" in stripped_line:
                has_chmod = True
                
            if stripped_line.startswith("COPY"):
                parts = stripped_line.split()
                if len(parts) >= 3:
                    src_item = parts[1].rstrip("/")
                    if src_item != "src" and not src_item.startswith("--") and not os.path.exists(os.path.join(dir_temp, src_item)):
                        continue
                        
            if "mkdir " in stripped_line and "mkdir -p" not in stripped_line:
                line = line.replace("mkdir ", "mkdir -p ")
            
            if (stripped_line.startswith("ENTRYPOINT") or stripped_line.startswith("CMD")) and not has_chmod:
                sanitized_lines.append("RUN chmod +x /usr/local/bin/*.sh 2>/dev/null || true")
                has_chmod = True
                
            sanitized_lines.append(line)
            
        with open(os.path.join(dir_temp, "Dockerfile"), "w", encoding="utf-8") as f:
            f.write('\n'.join(sanitized_lines))
            
    if data.get("docker_compose_yml"):
        with open(os.path.join(dir_temp, "docker-compose.yml"), "w", encoding="utf-8") as f:
            f.write(data["docker_compose_yml"])
            
    if data.get("writeup_md"):
        with open(os.path.join(dir_temp, "Writeup.md"), "w", encoding="utf-8") as f:
            f.write(data["writeup_md"])
            
    shutil.make_archive(dir_temp, 'zip', dir_temp)
    shutil.rmtree(dir_temp)
    
    print(f"\n[+] Professional Lab created successfully!")
    print(f"    Archive: {dir_temp}.zip")
    print(f"    To start: unzip {dir_temp}.zip && cd {dir_temp} && sudo docker-compose up -d --build")
