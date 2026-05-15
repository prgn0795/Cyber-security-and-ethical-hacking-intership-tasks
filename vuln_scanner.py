import requests
from bs4 import BeautifulSoup
import urllib.parse
import argparse

# Common payloads for basic vulnerability detection
SQLI_PAYLOADS = ["'", "' OR '1'='1", "' OR 1=1--", "' UNION SELECT NULL--"]
XSS_PAYLOADS = ["<script>alert('XSS')</script>", '"><script>alert(1)</script>']

def get_all_forms(url):
    """Fetch all HTML forms from the given URL."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find_all("form")
    except Exception as e:
        print(f"[-] Error fetching forms from {url}: {e}")
        return []

def form_details(form):
    """Extract form details like action, method, and input fields."""
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
        
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, value):
    """Submit a form with a specific payload."""
    target_url = urllib.parse.urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    
    for input_field in inputs:
        if input_field["type"] == "text" or input_field["type"] == "search":
            input_name = input_field.get("name")
            if input_name:
                data[input_name] = value
        elif input_field["type"] == "hidden":
            input_name = input_field.get("name")
            if input_name:
                data[input_name] = "hidden_value" # default safe value
                
    try:
        if form_details["method"] == "post":
            return requests.post(target_url, data=data, timeout=5)
        else:
            return requests.get(target_url, params=data, timeout=5)
    except Exception as e:
        print(f"[-] Error submitting form to {target_url}: {e}")
        return None

def test_sqli(url):
    """Test a URL for basic SQL injection vulnerabilities."""
    print(f"\n[*] Testing {url} for SQL Injection...")
    forms = get_all_forms(url)
    print(f"[*] Found {len(forms)} forms on {url}.")
    
    is_vulnerable = False
    for form in forms:
        details = form_details(form)
        for payload in SQLI_PAYLOADS:
            response = submit_form(details, url, payload)
            if response:
                # Basic check for common SQL error messages
                content = response.content.decode(errors='ignore').lower()
                errors = [
                    "you have an error in your sql syntax",
                    "warning: mysql",
                    "unclosed quotation mark after the character string",
                    "quoted string not properly terminated"
                ]
                for error in errors:
                    if error in content:
                        print(f"[+] SQL Injection VULNERABILITY DETECTED in form at {details['action']}")
                        print(f"    Payload: {payload}")
                        is_vulnerable = True
                        break
            if is_vulnerable:
                break
                
    if not is_vulnerable:
        print("[-] No SQL Injection vulnerabilities detected.")

def test_xss(url):
    """Test a URL for basic Cross-Site Scripting (XSS) vulnerabilities."""
    print(f"\n[*] Testing {url} for XSS...")
    forms = get_all_forms(url)
    print(f"[*] Found {len(forms)} forms on {url}.")
    
    is_vulnerable = False
    for form in forms:
        details = form_details(form)
        for payload in XSS_PAYLOADS:
            response = submit_form(details, url, payload)
            if response:
                # Basic check: if the raw payload is reflected in the response
                content = response.content.decode(errors='ignore')
                if payload in content:
                    print(f"[+] XSS VULNERABILITY DETECTED in form at {details['action']}")
                    print(f"    Payload: {payload}")
                    is_vulnerable = True
                    break
                    
    if not is_vulnerable:
        print("[-] No XSS vulnerabilities detected.")

def main():
    parser = argparse.ArgumentParser(description="Web Application Vulnerability Scanner")
    parser.add_argument("url", help="Target URL to scan (e.g., http://example.com)")
    parser.add_argument("--scan", choices=["sqli", "xss", "all"], default="all", help="Type of scan to perform")
    
    args = parser.parse_args()
    
    print("========================================")
    print("   WEB VULNERABILITY SCANNER STARTED    ")
    print("========================================")
    
    if args.scan in ["sqli", "all"]:
        test_sqli(args.url)
        
    if args.scan in ["xss", "all"]:
        test_xss(args.url)
        
    print("\n========================================")
    print("               SCAN COMPLETE            ")
    print("========================================")

if __name__ == "__main__":
    main()
