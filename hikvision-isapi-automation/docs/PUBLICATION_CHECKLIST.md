# Public-release checklist

## Mandatory checks BEFORE making this code public

- [ ] Obtain written approval from the software/copyright owner and any client whose confidential operational workflows may be represented.
- [ ] Review and remove remaining confidential architecture, hardening methods, device-management procedures and vendor-specific integration details, beyond simple secrets.
- [ ] Review source code, documentation, git history, branch/tag refs, screenshots, issue content, notebooks, compiled files and hidden files.
- [ ] Verify no secrets, personal data, organization identifiers, internal routes/addresses, device serials or operational examples remain.
- [ ] Ensure the original private script and historical commits were never imported into the future public repository.
- [ ] Rotate any credential or token that has ever already been exposed elsewhere.
- [ ] Confirm any cryptographic implementation constants used for device-import are shareable under your contracts/rights.
- [ ] Inspect and test all `verify=False` calls; use trusted certificate validation before real-world use.
- [ ] Validate the safety of `DRY_RUN` and all deletion/user-management/reboot operations on *your own isolated lab devices*.
- [ ] Run `python scripts/publish_check.py`, Python compilation and the mock tests.
- [ ] Confirm that `.gitignore` is in effect, and use `git status --short` and `git diff --cached` before pushing.
- [ ] Add an appropriate license only after ownership/publication rights are clear.

## Suggested repository setup

**Name:** `hikvision-isapi-automation`

**About:** `Python automation for Hikvision NVR and CCTV configuration using ISAPI, Excel and Selenium.`

**Topics:** `hikvision`, `isapi`, `cctv`, `nvr`, `python`, `automation`, `selenium`, `network-engineering`, `device-management`

**First tagged release:** `v0.1.0` (only after successful security, rights and lab testing).

## Publish via GitHub web interface

1. Create a new repository with the name above; choose **Private** until approvals and review are complete.
2. Upload only the sanitized project files (not the original script or operational data).
3. Double-check hidden files, source, examples, commit history and file upload selection.
4. Add topics, repository description and (later) a safe synthetic demo.
5. Switch to **Public** only when the mandatory review is completed.

## Publish via Git command line

From the newly extracted sanitized folder, **not** a clone or copy of an older private repository:

```powershell
git init -b main
python scripts/publish_check.py
git add .
git status --short
git diff --cached --stat
git commit -m "Initial sanitized release candidate"
git remote add origin https://github.com/YOUR-USERNAME/hikvision-isapi-automation.git
git push -u origin main
```

Create the empty GitHub repo first; do not initialize it with a conflicting README. Keep the remote **private** until cleared. Never push your original script as a prior commit, even temporarily.

## Increase discoverability (after release approval)

1. Write the first README screen for people scanning GitHub searches: one-line value proposition, concrete features, setup command and a screenshot/GIF made with synthetic data only.
2. Include the keyword people will search for: **Hikvision ISAPI Python**, **NVR configuration automation**, **bulk CCTV configuration**.
3. Add relevant GitHub topics and a descriptive About sentence.
4. Publish small, useful releases and post change logs; describe tested models/firmware without customer details.
5. Create easy-to-reproduce first issues for modularization, unit tests, safer TLS and logging.
6. Share a short technical walkthrough on GitHub Discussions, Reddit communities permitting project links, developer blogs and LinkedIn. Contribute genuinely; do not spam or request artificial stars.
7. Answer issues and publish verified examples with mock configurations; consistent maintenance earns long-term trust.

Stars are voluntary social signals; no technique can guarantee them.
