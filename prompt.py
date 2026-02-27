def build_prompt(target_vulnerability, include_writeup):
    prompt = f"""
    Act as a Senior Full-Stack Developer and AppSec Expert. 
    Your task is to create a HIGHLY REALISTIC, production-like vulnerable web application for a penetration testing lab.
    
    Vulnerabilities to seamlessly integrate: {target_vulnerability}.

    REQUIREMENTS FOR REALISM & EXPLOITABILITY:
    1. BUSINESS CONTEXT: The app MUST simulate a real-world corporate system (e.g., E-commerce, HR Portal, CRM).
    2. UI/UX: You MUST use a CSS framework via CDN (like Bootstrap) in the HTML.
    3. DUMMY DATA: Create an `init.sql` file to seed the database with realistic fake data.
    4. PLAUSIBLE FLAWS: Embed vulnerabilities naturally within business logic. Hide a FLAG{{...}}.
    5. FULL SOURCE CODE: Generate COMPLETE PHP/HTML source code inside the `src/` directory. No placeholders.
    6. NO AUTH WALLS: Vulnerable features MUST be accessible WITHOUT requiring valid login credentials.
    7. STRICTLY NO ACCIDENTAL MITIGATIONS (CRITICAL): Do NOT use prepared statements (unless demonstrating how to bypass them), `htmlspecialchars()`, `strip_tags()`, `mysqli_real_escape_string()`, or ANY input sanitization on the vulnerable parameters. The vulnerability MUST be 100% exploitable with standard payloads.
    
    CRITICAL DOCKER RULES (ABSOLUTELY STRICT):
    1. DB HOSTNAME: In PHP connection code, the host MUST be exactly 'db', NEVER 'localhost'.
    2. MYSQL ENV VARS: In `docker-compose.yml`, the database MUST include `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, and `MYSQL_PASSWORD`.
    3. INIT.SQL MOUNT: In `docker-compose.yml`, mount exactly as: `- ./init.sql:/docker-entrypoint-initdb.d/init.sql`.
    4. WEB DOCKERFILE: Use `FROM php:8.1-apache`. Use `RUN docker-php-ext-install mysqli pdo pdo_mysql`.
    5. NO INFINITE LOOPS: DO NOT write `sleep` or `while` loops in entrypoints. Start Apache directly (`exec apache2-foreground`).
    
    OUTPUT FORMAT INSTRUCTIONS:
    Every single file must start with `==FILE: path/to/file.ext==` and end with `==ENDFILE==`. DO NOT TRUNCATE.
    
    Example format:
    ==FILE: src/index.php==
    <?php echo "Code here"; ?>
    ==ENDFILE==
    """
    return prompt
