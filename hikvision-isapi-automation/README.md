# Hikvision ISAPI Device Configuration Automation

**Python • Hikvision ISAPI • Multi-device NVR & CCTV configuration • Excel inventory • Selenium**

Automate repetitive, authorized Hikvision device-administration tasks across NVRs, dome cameras, and other supported cameras. The program reads device settings from a local Excel workbook, applies configuration through Hikvision ISAPI and selected browser workflows, and saves diagnostics and result reports locally.

> [!IMPORTANT]
> **PUBLIC-RELEASE CANDIDATE — NOT APPROVED OR HARDWARE-VERIFIED.** This repository is a sanitized derivative of a large existing script. Sanitization does **not** establish ownership or permission to publish it. Before setting the repository to public, obtain the rights holder's approval, review the exposed architecture and protocol behavior, and run your own security assessment. This software can change credentials, network settings, certificates, and camera channels.

## Features

| Area | What it can do |
|---|---|
| Device discovery and inventory | Load NVR, dome and discreet-camera rows from an Excel workbook |
| ISAPI configuration | Hostnames, OSD names, time synchronization, NTP and compatible image settings |
| Device parameter import | Optional NVR/camera settings import with compatibility workflows |
| Certificate operations | Generate CSRs, create/select certificates, verify HTTPS-related bindings |
| NVR management | Sync NVR camera records with matching cameras and configure stream parameters |
| User administration | Optional account creation, role-based permission configuration and password rotation |
| Browser automation | Microsoft Edge / Selenium fallbacks for firmware-specific UI controls |
| Verification | Read-back checks, CSV reports, diagnostic backups, bounded retries |
| Concurrency | Parallel camera tasks with worker caps and locks around shared local plugins |

## Safety model

- **Device access is blocked until you explicitly opt in** via `HIKVISION_AUTHORIZE_DEVICE_ACCESS=YES`.
- The public version defaults to `HIKVISION_DRY_RUN=true`. **Do not assume dry-run means absolutely no network writes** without auditing every workflow; this large codebase has not been exhaustively verified.
- Deleting default certificates and extra NVR channels is disabled by default in the sanitized source.
- Device administrator passwords and other account passwords are read from **your private Excel workbook**, not included here. Never commit your populated workbook.
- Certificate subject fields, certificate ID, local paths, and device-import key material are read from environment variables.
- Some HTTP paths in the existing code use `verify=False` (TLS verification disabled). Use only in an isolated, authorized test lab until fixed.
- The `backup/`, `report/`, `CSR/`, `cert_payload/`, and `web_ui_debug/` folders may contain secrets or identifiers. They are ignored by Git.

## Requirements

- Python 3.10+ (Windows recommended for native Hikvision plugin/file-dialog compatibility)
- `requests`, `urllib3`, `openpyxl`, `selenium`, and an optional supported AES backend
- Microsoft Edge for Selenium automation
- Access to your **own or explicitly authorized** Hikvision test devices
- Firmware compatibility varies; functions that work on one model may fail on another
- Native Device Parameter Config import may require the manufacturer's local `GWebPluginService`, which is **not bundled**

## Quick start on Windows

### 1. Clone the repository and install dependencies

```powershell
git clone https://github.com/YOUR-USERNAME/hikvision-isapi-automation.git
cd hikvision-isapi-automation
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Prepare your **local-only** workbook

The script expects an Excel file with device tabs including `NVR_Settings`, `Dome_Settings`, and `Discreet_Settings`. Essential inventory columns include `Site ID`, `Current IP`, `Username`, `Password`, `Hostname`, and `Camera Type`.

A **demonstration-only schema** is supplied at `examples/devices.example.xlsx`. It intentionally contains no operational credentials or reachable device addresses. A working deployment also requires the appropriate configuration, security, account, and permissions tabs filled out for your selected workflow and firmware. This is **not** a complete replacement for a tested production configuration workbook.

Create a folder named `local_data` and save your private device workbook as `local_data/devices.xlsx`. Keep real device parameter files and credentials there, not in the repository.

### 3. Configure your local settings

```powershell
# Example locations only; never commit actual paths, IP lists or credentials.
$env:HIKVISION_WORKDIR = (Join-Path (Get-Location) 'local_data')
$env:HIKVISION_DEVICES_EXCEL = (Join-Path $env:HIKVISION_WORKDIR 'devices.xlsx')

# Set site-specific certificate fields for YOUR organization, locally:
$env:HIKVISION_CERT_ID = 'MY_TEST_CERT'
$env:HIKVISION_CERT_COUNTRY = 'US'
$env:HIKVISION_CERT_STATE = 'Example State'
$env:HIKVISION_CERT_LOCALITY = 'Example City'
$env:HIKVISION_CERT_ORGANIZATION = 'Example Organization'
$env:HIKVISION_CERT_ORG_UNIT = 'Device Lab'
$env:HIKVISION_CERT_EMAIL = 'operator@example.invalid'

# Optional, for authorized direct configuration-file import ONLY:
# $env:HIKVISION_IMPORT_KDF_SUFFIX = '<YOUR_AUTHORIZED_PRIVATE_VALUE>'
```

Real administrator and service-account passwords belong **only in the local workbook** (or a future secrets manager), not in these commands or in GitHub. Since Excel is not encrypted by this script, protect it with appropriate file permissions/disk encryption.

### 4. Confirm your options before connecting to a device

Review the toggles at the top of `hikvision_config.py`, especially `WORKFLOW_START_MODE`, account management, certificate deletion, camera-channel deletion, native plugin import, and parallelism.

Run the built-in public-file scan first:

```powershell
python scripts/publish_check.py
python -m py_compile hikvision_config.py
```

Only in your authorized, isolated environment:

```powershell
$env:HIKVISION_AUTHORIZE_DEVICE_ACCESS = 'YES'
$env:HIKVISION_DRY_RUN = 'true'
python hikvision_config.py
```

After independent review and testing, you can set `HIKVISION_DRY_RUN=false` to allow the code paths that check that flag to apply changes. The authorization gate remains required. **Do not run this on live deployed devices until you validate each operation and have a recovery plan.**

## Example layout

```text
hikvision-isapi-automation/
├── hikvision_config.py        # Sanitized program
├── examples/
│   └── devices.example.xlsx   # Dummy data / schema illustration ONLY
├── scripts/
│   └── publish_check.py      # Basic local disclosure checks
├── docs/
│   └── PUBLICATION_CHECKLIST.md
├── .github/workflows/check.yml
├── .gitignore
├── requirements.txt
└── README.md

# Generated locally, never committed:
local_data/
├── devices.xlsx               # YOUR PRIVATE DEVICE LIST, NOT PUBLIC
├── backup/
├── report/
├── CSR/
├── cert_payload/
└── web_ui_debug/
```

## Known limitations

1. **Not yet regression-tested** against the original workbook or a real Hikvision lab after anonymization. Syntax and offline checks are not evidence of correct device operation.
2. The program is large and firmware-specific; some automation uses absolute XPaths which can break after firmware changes.
3. Several request paths disable TLS certificate verification; do not expose device credentials across untrusted links.
4. Account and network changes can interrupt device access; some workflows reboot devices or delete default configuration objects.
5. The example workbook is a schema illustration, not a complete validated template for all advanced passes.
6. The program's certificate-import key-derivation value has been removed from the public source. Operators must provide their own authorized value when using that feature.
7. No license is provided until the copyright holder authorizes a public/open-source release.

## Roadmap / good first issues

- [ ] Split the monolithic program into `api/`, `certificates/`, `nvr/`, `web_ui/`, and `reports/` modules
- [ ] Introduce a strict `DeviceClient` with proper certificate validation and credential-safe logging
- [ ] Build mocked ISAPI tests with safe dummy XML and golden-response fixtures
- [ ] Add a full **synthetic** workbook fixture and automated integration tests
- [ ] Add resumable task status and safer dry-run coverage across every workflow
- [ ] Add support matrix by firmware/device model without publishing client deployments
- [ ] Build a demo GIF using virtual/mock data only

## Contributing and support

Open a GitHub issue with a **redacted** description, reproducible steps and safe dummy responses. Do not include real IPs, usernames, passwords, server certificates, vendor tokens, company identifiers, or screenshots of production environments. See [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

*Independent community example; not officially affiliated with or endorsed by Hikvision.*
