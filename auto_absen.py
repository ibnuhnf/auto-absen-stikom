# Ganti bagian ini
service = Service(ChromeDriverManager().install())  # <-- ini sering gagal di Actions

# Jadi seperti ini (pakai pre-installed chromedriver)
from selenium.webdriver.chrome.service import Service as ChromeService
import os

# Path chromedriver di ubuntu-latest GitHub Actions (versi terbaru 2026 biasanya /usr/bin/chromedriver)
chromedriver_path = "/usr/bin/chromedriver"  # atau "/usr/local/bin/chromedriver" kalau beda

if not os.path.exists(chromedriver_path):
    chromedriver_path = "/usr/local/bin/chromedriver"  # fallback

service = ChromeService(executable_path=chromedriver_path)

# Opsi Chrome tambahan untuk Actions (penting!)
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")              # WAJIB di Actions
options.add_argument("--disable-dev-shm-usage")   # WAJIB, hindari crash memory
options.add_argument("--disable-gpu")             # sering dibutuhkan
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--window-size=1920,1080")   # hindari resize error

driver = webdriver.Chrome(service=service, options=options)
