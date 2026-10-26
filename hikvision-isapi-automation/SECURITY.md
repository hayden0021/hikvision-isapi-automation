# Security policy

This project configures physical network devices and may handle sensitive credentials. **Do not open a public GitHub issue containing security vulnerabilities with exploit details, active credentials, production IPs, configuration backups, or certificates.** Use GitHub's private vulnerability reporting where enabled.

Operate only with authorization and on isolated test devices. Do not publish operational workbooks or reports. Consider every printed response, backup XML, screenshot and CSR output sensitive until assessed.

## Current high-priority concerns

- TLS verification is disabled in parts of the inherited HTTP code (`verify=False`). This can permit man-in-the-middle exposure of credentials. Fix before using over untrusted networks.
- The dry-run mode has not been comprehensively proven non-mutating; check all device mutation paths.
- Sensitive credentials are currently loaded from a plaintext local workbook. Lock it down and consider secrets-manager integration.
- Legacy API, browser automation and device-parameter import are firmware-specific and not independently tested across models.
- Deleting default certificates or channels could cause outages; retain backups and a recovery path.

If a secret is accidentally published, **revoke or rotate it immediately**, clean the repository history as appropriate, and follow GitHub's incident guidance.
