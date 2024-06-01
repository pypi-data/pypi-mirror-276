import os
import requests
import zipfile

def download_chromedriver():
    chromedriver_url = "https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.60/win64/chromedriver-win64.zip"
    chromedriver_zip_path = "chromedriver-win64.zip"
    chromedriver_exe_path = "chromedriver-win64/chromedriver.exe"
    
    if not os.path.exists(chromedriver_exe_path):
        print("Downloading chromedriver...")
        response = requests.get(chromedriver_url)
        with open(chromedriver_zip_path, "wb") as f:
            f.write(response.content)
        
        with zipfile.ZipFile(chromedriver_zip_path, 'r') as zip_ref:
            zip_ref.extractall('.')
        
        os.remove(chromedriver_zip_path)
