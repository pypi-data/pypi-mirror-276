from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def professor_driver(proxy_server, blocked_sites=None):
    """
    Creates a configured instance of Chrome WebDriver with the option to block specific websites.

    Args:
    proxy_server (str): Proxy server address.
    blocked_sites (list of str): List of hostnames to block.

    Returns:
    webdriver.Chrome: Configured Chrome WebDriver.
    """
    current_dir = os.path.dirname(__file__)
    extension_path = os.path.join(current_dir, 'data', 'hlifkpholllijblknnmbfagnkjneagid.crx')

    options = Options()
    options.add_extension(extension_path)
    options.add_argument(f'--proxy-server={proxy_server}')

    # Dynamically add host rules for blocking sites
    if blocked_sites:
        for site in blocked_sites:
            options.add_argument(f"--host-rules=MAP {site} 0.0.0.0")
 
    return webdriver.Chrome(options=options)
