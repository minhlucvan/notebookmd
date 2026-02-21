# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.3.x   | :white_check_mark: |
| < 0.3   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in notebookmd, please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, please report vulnerabilities by emailing the maintainers or using
[GitHub's private vulnerability reporting](https://github.com/minhlucvan/notebookmd/security/advisories/new).

### What to Include

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgment:** Within 48 hours
- **Initial assessment:** Within 1 week
- **Fix and release:** Dependent on severity, typically within 2 weeks for critical issues

## Security Considerations

notebookmd generates Markdown files from Python code. Key security notes:

- **File paths:** The library writes to user-specified file paths. Ensure output paths are trusted.
- **User input in reports:** If your reports include user-provided data, be mindful of Markdown injection (e.g., unexpected links or HTML in rendered Markdown).
- **Dependencies:** The core package has zero dependencies. Optional extras (pandas, matplotlib) are well-established libraries with their own security practices.
