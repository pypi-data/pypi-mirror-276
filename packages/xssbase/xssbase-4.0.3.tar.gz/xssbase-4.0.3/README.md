# XSSbase

XSSbase is a professional tool designed to help web developers scan for Cross-Site Scripting (XSS) vulnerabilities. It automates the process of testing web applications for XSS vulnerabilities by using a set of predefined payloads or custom payloads provided by the user.

- **Full Documentation**: <a href="https://bytebreach.github.io/pdf/xssbase-Full-Commands.pdf">Link</a>
- **Basic XSS (Cross-Site Scripting) Vulnerable HTML Code**: <a href="https://github.com/ByteBreach/xssbase-test">Link</a>

## Features

- **Automated XSS Testing**: Scans web applications for XSS vulnerabilities using a list of predefined or user-specified payloads.
- **Platform Support**: Currently supports Windows.
- **Custom Payloads**: Allows users to provide their own payloads for testing.
- **Error Handling**: Handles stale element reference errors gracefully and retries automatically.
- **Comprehensive Reports**: Provides detailed information about detected XSS vulnerabilities.
- **Payload List URL**: Displays a URL to a list of useful XSS payloads.

## Benefits

- **Time-Saving**: Automates the tedious process of testing for XSS vulnerabilities, saving developers valuable time.
- **Improved Security**: Helps in identifying and fixing XSS vulnerabilities, enhancing the overall security of web applications.
- **Customizable**: Users can use their own payloads for testing, making it highly customizable for specific needs.

## Payload Examples

Here are a few sample XSS payloads that XSSbase can use:

1. `<script>alert('XSS')</script>`
2. `<img src=x onerror=alert('XSS')>`
3. `<svg onload=alert('XSS')>`
4. `"><script>alert('XSS')</script>`
5. `<body onload=alert('XSS')>`

For a comprehensive collection of XSS payloads, refer to the [payloadbox XSS payload list](https://github.com/payloadbox/xss-payload-list/blob/master/Intruder/xss-payload-list.txt).

## Payload List

A comprehensive list of useful XSS payloads is available at: <a href="https://mrfidal.in/cyber-security/xssbase/payload-list.html">Click Here</a>

## Installation

Currently, XSSbase is only compatible with Windows. To install, use the following command:

```sh
pip install xssbase
```

## Usage

### Basic Usage

To test a URL for XSS vulnerabilities using the predefined payloads:
```sh
xssbase --url <URL>
```
### Using Custom Payloads

To test a URL for XSS vulnerabilities using custom payloads from a file:
```sh
xssbase --url <URL> --payload <payload-file.txt>
```
### Example

To test http://example.com for XSS vulnerabilities using predefined payloads:
```sh
xssbase --url http://example.com
```
To test http://example.com for XSS vulnerabilities using payloads from `custom-payloads.txt`:
```sh
xssbase --url http://example.com --payload custom-payloads.txt
```

### Arguments

`--url`: The URL to test for XSS vulnerabilities (required).

`--payload`: The file containing custom XSS payloads (optional).


### License
This project is licensed under the MIT <a href="https://pypi.org/project/xssbase/#description">License</a>. See the LICENSE file for details.

### Disclaimer
This tool is intended for educational purposes and for use by web developers to secure their own applications. Unauthorized or malicious use is strictly prohibited.
