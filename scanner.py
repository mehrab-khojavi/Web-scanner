import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scan_website(url):
    try:
        # 웹 페이지 콘텐츠 가져오기
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(f"🔍 스캔 중: {url}")
        
        # 모든 링크 검사
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            
            # 깨진 링크 확인
            try:
                link_status = requests.head(full_url, allow_redirects=True).status_code
                if link_status == 404:
                    print(f"❌ 깨진 링크 발견: {full_url}")
            except:
                print(f"⚠️ 요청 실패: {full_url}")
            
            # 외부 링크 경고
            if link['href'].lower().startswith(('http://', 'https://')) and not url in link['href']:
                print(f"⚠️ 외부 링크 (잠재적 위험): {full_url}")

        # CSRF 토큰이 없는 form 확인
        for form in soup.find_all('form'):
            if not form.find('input', {'type': 'hidden', 'name': 'csrf_token'}):
                print(f"🚨 CSRF 보호 없는 양식 감지됨: {form}")

    except Exception as e:
        print(f"❗ 스캔 중 오류 발생: {e}")

# 실행 예시
if __name__ == "__main__":
    target_url = input("스캔할 URL을 입력하세요 (예: https://example.com): ")
    scan_website(target_url)
  Add main scanner script
