# Contributing

Please propose changes against a test fixture or synthetic device environment. Include a clear description, affected firmware/model (when public information), expected vs. actual behavior, and offline tests.

Before submitting a pull request:

1. Run `python scripts/publish_check.py` and `python -m py_compile hikvision_config.py`.
2. Remove organization names, real IPs, hostnames, certificate subjects, people, passwords, private file paths and authentic device log output.
3. Keep `.xlsx` files containing real device data, export reports, debugging screenshots and certificates out of Git.
4. Avoid breaking changes to the original ISAPI protocol fields; add regression tests for schema changes.
5. Do not run integration tests against public IPs, external networks or devices you do not control.

This project currently has no open-source license. Contributions should wait until code ownership and licensing are settled.
