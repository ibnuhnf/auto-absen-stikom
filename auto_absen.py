from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import sys
import os

USERNAME = "14524301"
PASSWORD = "1"
LOKASI   = ""
NTFY_TOPIC = "absenstikom14524301"   # Ganti kalau beda

CLASS_NAME = sys.argv[1] if len(sys.argv) > 1 else "Metode Numerik"

def kirim_notifikasi(pesan):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    try:
        requests.post(url, data=pesan.encode('utf-8'), timeout=10)
    except:
        pass

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--window-size=1920,1080")

# Pakai chromedriver pre-installed di GitHub Actions
chromedriver_path = "/usr/bin/chromedriver"
if not os.path.exists(chromedriver_path):
    chromedriver_path = "/usr/local/bin/chromedriver"

service = ChromeService(executable_path=chromedriver_path)

driver = webdriver.Chrome(service=service, options=options)

def lakukan_login():
    driver.get("https://siakad.stikompoltekcirebon.ac.id/index.php")
    time.sleep(5)
    wait = WebDriverWait(driver, 20)
    inputs = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
    inputs[0].clear(); inputs[0].send_keys(USERNAME)
    inputs[1].clear(); inputs[1].send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' or @value='MASUK'] | //button[contains(text(),'MASUK')]"))).click()
    time.sleep(7)

try:
    lakukan_login()
    lakukan_login()
    driver.get("https://siakad.stikompoltekcirebon.ac.id/dashboard.php?module=home")
    time.sleep(8)
    
    absen_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "ABSEN")))
    driver.execute_script("arguments[0].scrollIntoView(true);", absen_btn)
    time.sleep(1)
    absen_btn.click()
    
    pesan = f"✅ Absen {CLASS_NAME} BERHASIL pukul {time.strftime('%H:%M')}"
    kirim_notifikasi(pesan)
    print(pesan)
except Exception as e:
    pesan = f"❌ Absen {CLASS_NAME} GAGAL pukul {time.strftime('%H:%M')} - Error: {str(e)[:200]}"
    kirim_notifikasi(pesan)
    print(pesan)
finally:
    driver.quit()
