import argparse
import os
import sys
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from .main import test_xss_payloads, xss_payloads_default
from .utils import download_chromedriver

def main():
    # Check if the operating system is Windows
    if platform.system() != 'Windows':
        print("This tool only supports Windows.")
        sys.exit(1)

    # Define the argument parser
    parser = argparse.ArgumentParser(
        description="XSSbase - A professional tool for scanning XSS vulnerabilities.",
        epilog="Author: Fidal\nGitHub: https://github.com/mr-fidal\n\n"
               "Copyright 2024 Fidal. All rights reserved. \n"
               "payload list : https://mrfidal.in/cyber-security/xssbase/payload-list.html"
               "Unauthorized copying of this tool, via any medium is strictly prohibited."
    )
    parser.add_argument('--url', required=True, help='URL to test for XSS vulnerability')
    parser.add_argument('--payload', help='File containing XSS payloads to use')
    args = parser.parse_args()

    # Check if the payload file exists
    if args.payload and not os.path.exists(args.payload):
        print("Error: The specified payload file does not exist. Please add a valid file.")
        sys.exit(1)

    # Download the chromedriver if it doesn't exist
    download_chromedriver()

    # Set up Chrome WebDriver
    service = Service('chromedriver-win64/chromedriver.exe')  # Specify the path to chromedriver executable
    driver = webdriver.Chrome(service=service)

    # Load payloads
    if args.payload:
        with open(args.payload, 'r', encoding='utf-8') as f:
            payloads = [line.strip() for line in f.readlines()]
    else:
        payloads = xss_payloads_default

    try:
        # Test XSS payloads
        test_xss_payloads(driver, args.url, payloads)
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
