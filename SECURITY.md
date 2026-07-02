# Security Policy

## 🔒 Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🚨 Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Publicly Disclose
Please do not open a public issue. Security vulnerabilities should be reported privately.

### 2. Contact Us
Send details to: **[Your Email]** or create a private security advisory on GitHub.

### 3. Include Details
- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue

### 4. Response Time
- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Fix Timeline**: Depends on severity

## 🛡️ Security Best Practices

When using AgriVit-Sentinel:

1. **Never commit sensitive data** (API keys, passwords, credentials)
2. **Use environment variables** for sensitive configuration
3. **Keep dependencies updated** regularly
4. **Review uploaded files** before processing
5. **Use HTTPS** in production environments
6. **Implement rate limiting** for API endpoints
7. **Sanitize user inputs** to prevent injection attacks

## 🔐 Known Security Considerations

- File uploads are restricted to image types (JPEG, PNG)
- Input validation is performed on all user-submitted data
- Model files are served from protected directories

## 📜 Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find similar problems
3. Prepare fixes for all supported versions
4. Release patches and publish security advisory

---

Thank you for helping keep AgriVit-Sentinel and its users safe!
