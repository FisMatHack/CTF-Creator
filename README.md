CTF-Creator: Vulnerable Lab Generator

## What it does
CTF-Creator is a command-line tool that instantly generates highly realistic, Dockerized web applications tailored with specific or randomized vulnerabilities. It creates the vulnerable source code, the database initialization scripts, the Dockerfiles, and packages everything into a deployable `.zip` file. Optionally, it generates a precise step-by-step Markdown Writeup based exactly on the generated code.

## Who it helps
This project is built for the **OffSec Community**, specifically students preparing for the OSCP, OSWE, or practicing in Proving Grounds. Finding labs to practice a very specific vulnerability or bypassing a specific filter can be tedious. CTF-Creator provides infinite, offline practice environments so students can hone their methodology and "Try Harder" on their own terms.

## How AI is used
The core engine relies on an LLM (Large Language Model) utilizing Advanced Prompt Engineering and Prompt Chaining to act as a Senior AppSec Engineer. 
* **Dynamic Code Generation:** The AI writes realistic business logic (like HR portals or E-commerce sites) and seamlessly embeds vulnerabilities without artificial security filters.
* **Infrastructure as Code:** The AI writes strict `docker-compose.yml` and `Dockerfile` configurations, ensuring the lab boots up flawlessly with proper database handling.
* **Self-Auditing Writeups:** Through a secondary chained prompt, the AI reads its own generated code to produce an accurate, 100% exploitable Writeup, completely eliminating AI hallucinations and generic payloads.

## Key Features
* **Targeted Practice:** Request specific vulnerabilities via CLI (e.g., `-v "SQLi and IDOR"`).
* **Blind Roulette:** Test your enumeration skills by asking for random vulnerabilities (e.g., `-v "random-3"`).
* **Zero-Config Deployment:** Outputs a ready-to-run `.zip` environment.
* **Writeup Mode:** Generates a detailed Context, Exploitation, and Remediation guide (`-w` flag).

## Installation
1. Clone the repository:
   `git clone https://github.com/FisMatHack/CTF-Creator`
2. Navigate to the directory:
   `cd CTF-Creator`
3. Install the required dependencies:
   `pip install google-genai --break-system-packages`
4. Export your API Key as an environment variable (or add it to your `.env` file):
   `export GEMINI_API_KEY="your_api_key_here"`

## Usage

Generate a lab with a specific vulnerability and include a Writeup:
`python3 main.py -v "SQLi" -n my_sqli_lab -w`

Generate a challenging lab with 3 random vulnerabilities:
`python3 main.py -v "random-3" -n random_challenge -w`

Deploy the generated lab:
`unzip lab_my_sqli_lab.zip`
`cd lab_my_sqli_lab`
`sudo docker-compose up -d --build`
