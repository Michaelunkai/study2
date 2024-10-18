from flask import Flask, render_template, request
import requests
from urllib.parse import urljoin

app = Flask(__name__)

class WebVulnScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.vulnerabilities = []

    def check_sql_injection(self):
        payloads = ["' OR '1'='1", "' OR '1'='1' --", '" OR "1"="1']
        for payload in payloads:
            test_url = urljoin(self.target_url, f"?id={payload}")
            try:
                response = requests.get(test_url, verify=False)  # Bypass SSL verification
                if "error" in response.text.lower() or "syntax" in response.text.lower():
                    self.vulnerabilities.append({
                        "vuln": "SQL Injection",
                        "url": test_url,
                        "description": (
                            "SQL Injection allows attackers to manipulate database queries by injecting malicious SQL code. "
                            "This can lead to data exposure, modification, or deletion."
                        ),
                        "fix_steps": [
                            "1. Ensure that the application uses prepared statements with parameterized queries in the database interaction code.",
                            "2. For Python applications using MySQL, install `mysql-connector-python`:",
                            "`pip install mysql-connector-python`",
                            "3. Modify the database queries to use parameterized queries. Example (Python):",
                            "",
                            "4. Ensure all user inputs are validated and sanitized to prevent direct injection."
                        ]
                    })
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")

    def check_xss(self):
        payloads = ["<script>alert('xss')</script>", "'><script>alert(1)</script>"]
        for payload in payloads:
            test_url = urljoin(self.target_url, f"?search={payload}")
            try:
                response = requests.get(test_url, verify=False)  # Bypass SSL verification
                if payload in response.text:
                    self.vulnerabilities.append({
                        "vuln": "Cross-Site Scripting (XSS)",
                        "url": test_url,
                        "description": (
                            "XSS allows attackers to inject malicious scripts into web pages viewed by other users. "
                            "It can be used to steal cookies, session tokens, or sensitive data."
                        ),
                        "fix_steps": [
                            "1. Ensure user inputs are properly escaped before rendering them on web pages.",
                            "2. Use a templating engine that automatically escapes output. For example, Jinja2 in Flask automatically escapes data.",
                            "3. Install Flask with Jinja2 support:",
                            "`pip install Flask`",
                            "4. Validate user input to ensure no HTML or script tags are allowed, or sanitize input using libraries like `bleach`:",
                            "`pip install bleach`",
                            "Example usage:",
                            ""
                        ]
                    })
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")

    def check_csrf(self):
        try:
            response = requests.get(self.target_url, verify=False)  # Bypass SSL verification
            if "csrf_token" not in response.text:
                self.vulnerabilities.append({
                    "vuln": "Cross-Site Request Forgery (CSRF)",
                    "url": self.target_url,
                    "description": (
                        "CSRF tricks users into performing actions on a website without their consent. "
                        "An attacker can hijack user sessions and perform malicious actions on their behalf."
                    ),
                    "fix_steps": [
                        "1. Implement CSRF protection using tokens in forms and HTTP requests.",
                        "2. If using Flask, install the `Flask-WTF` extension for CSRF protection:",
                        "`pip install Flask-WTF`",
                        "3. Add CSRF protection in your app. Example (Flask):",
                        "",
                        "4. Ensure all forms include CSRF tokens, and validate these tokens on the server-side."
                    ]
                })
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    def run(self):
        self.check_sql_injection()
        self.check_xss()
        self.check_csrf()
        return self.vulnerabilities

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target_url = request.form['url']
        scanner = WebVulnScanner(target_url)
        vulnerabilities = scanner.run()
        return render_template('results.html', vulnerabilities=vulnerabilities, target_url=target_url)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
