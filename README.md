import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# تابع برای ارسال درخواست و بررسی لینک‌ها
def check_links(url):
    try:
        # ارسال درخواست به URL
        response = requests.get(url)
        
        # چک کردن وضعیت پاسخ
        if response.status_code != 200:
            print(f"[!] {url} is not reachable. Status Code: {response.status_code}")
            return
        
        # تجزیه محتوای HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج تمام لینک‌ها از صفحه
        links = set()
        for anchor in soup.find_all('a', href=True):
            link = anchor['href']
            full_link = urljoin(url, link)  # تبدیل لینک‌های نسبی به مطلق
            links.add(full_link)
        
        # بررسی لینک‌ها
        for link in links:
            try:
                link_response = requests.get(link)
                if link_response.status_code != 200:
                    print(f"[!] Broken link: {link} Status Code: {link_response.status_code}")
                else:
                    print(f"[+] {link} is working fine!")
            except requests.exceptions.RequestException as e:
                print(f"[!] Error checking link: {link} Error: {e}")
    
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to reach {url} Error: {e}")

# ورود URL سایت برای بررسی
if __name__ == "__main__":
    target_url = input("Enter the URL to scan: ")
    check_links(target_url)
