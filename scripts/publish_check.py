"""Basic OFFLINE check for obvious secrets and mistaken private files.

This is not a substitute for professional review or GitHub secret scanning.
"""
from __future__ import annotations

from pathlib import Path
import ipaddress
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_EXAMPLE = ROOT / 'examples' / 'devices.example.xlsx'
ALLOWED_FILES = {'README.md', 'CONTRIBUTING.md', 'SECURITY.md'}
RULES = [
    ('Windows home-directory path', re.compile(r'[A-Za-z]:\\\\?Users\\\\?[^\\\\\s"\']+', re.I)),
    ('Email address outside reserved examples', re.compile(r'\b[A-Za-z0-9._%+-]+@(?!example\.invalid\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', re.I)),
    ('PEM private key header', re.compile(r'-{5}BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-{5}')),
    ('GitHub credential format', re.compile(r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b')),
    ('AWS access key format', re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
    ('Apparent literal password assignment', re.compile(r'(?i)^\s*(?:password|passwd|api_key|api_secret)\s*=\s*[\'\"][^\'\"]{6,}[\'\"]\s*$')),
]
EXTENSIONS = {'.py', '.md', '.yml', '.yaml', '.txt', '.example'}
BAD_EXTENSIONS = {'.pfx', '.p12', '.key', '.pem', '.csr', '.crt', '.cer', '.sqlite', '.sqlite3', '.db', '.har', '.pcap', '.pcapng', '.bak'}
BAD_DIRS = {'local_data', 'backup', 'report', 'CSR', 'cert_payload', 'web_ui_debug'}
issues = []

for file in ROOT.rglob('*'):
    if not file.is_file():
        continue
    rel = file.relative_to(ROOT)
    if any(part in {'.git', '.venv', '__pycache__'} for part in rel.parts):
        continue
    if any(part in BAD_DIRS for part in rel.parts):
        continue  # local-only data ignored by git, check staged files independently
    if file.name == 'publish_check.py':
        continue  # scanner regex strings must not trigger their own rules
    if file.suffix.lower() == '.xlsx' and file != ALLOWED_EXAMPLE:
        issues.append(f'{rel}: unexpected workbook')
    if file.suffix.lower() in BAD_EXTENSIONS:
        issues.append(f'{rel}: sensitive file extension')
    if file.suffix.lower() not in EXTENSIONS:
        continue
    try:
        content = file.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        issues.append(f'{rel}: unexpected binary text file')
        continue
    for label, pattern in RULES:
        for hit in pattern.finditer(content):
            issues.append(f'{rel}:{content.count(chr(10), 0, hit.start())+1}: {label}')
    # Flag public or non-example IP literals. RFC 5737 documentation IPs, loopback,
    # wildcard and isolated RFC 1918 examples do not indicate a deployed site.
    for hit in re.finditer(r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])', content):
        try:
            ip = ipaddress.ip_address(hit.group())
        except ValueError:
            continue
        if not (ip.is_loopback or ip.is_unspecified or ip.is_private):
            issues.append(f'{rel}:{content.count(chr(10), 0, hit.start())+1}: nonprivate IPv4 literal')

if issues:
    print('WARNING: public-file audit found items requiring manual review:')
    for issue in issues:
        print('-', issue)
    sys.exit(1)
print('Basic public-file checks passed. This does NOT certify absence of confidential material.')
