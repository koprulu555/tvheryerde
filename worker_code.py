import requests, json, gzip
from io import BytesIO
from datetime import datetime

def get_canli_tv_m3u():
    url = "https://core-api.kablowebtv.com/api/channels"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://tvheryerde.com",
        "Origin": "https://tvheryerde.com",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJjZ2QiOiIwOTNkNzIwYS01MDJjLTQxZWQtYTgwZi0yYjgxNjk4NGZiOTUiLCJkaSI6IjBmYTAzNTlkLWExOWItNDFiMi05ZTczLTI5ZWNiNjk2OTY0MCIsImFwdiI6IjEuMC4wIiwiZW52IjoiTElWRSIsImFwbiI6IjEwMDAiLCJzcGdkIjoiYTA5MDg3ODQtZDEyOC00NjFmLWI3NmItYTU3ZGViMWI4MGNjIiwiaWNoIjoiMCIsInNnZCI6ImViODc3NDRjLTk4NDItNDUwNy05YjAhLTQ0N2RmYjg2NjJhZCIsImlkbSI6IjAiLCJkY3QiOiIzRUY3NSIsImlhIjoiOjpmZmZmOjEwLjAuMC41IiwiY3NoIjoiVFJLU1QiLCJpcGIiOiIwIn0.bT8PK2SvGy2CdmbcCnwlr8RatdDiBe_08k7YlnuQqJE"
    }
    params = {"ipb": "0"}
    
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] API isteği...")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        if response.headers.get('Content-Encoding') == 'gzip':
            with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
                content = gz.read().decode('utf-8')
        else:
            content = response.content.decode('utf-8')
        
        data = json.loads(content)
        
        if not data.get('IsSucceeded') or not data.get('Data', {}).get('AllChannels'):
            print("❌ API geçersiz yanıt")
            return None
        
        channels = data['Data']['AllChannels']
        print(f"✅ {len(channels)} kanal bulundu")
        
        m3u_content = "#EXTM3U\n#EXTENC:UTF-8\n#PLAYLIST:TVHerYerde\n"
        m3u_content += f"#GENERATED:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        kanal_sayisi = 0
        
        for idx, channel in enumerate(channels, 1):
            name = channel.get('Name', '').strip()
            hls_url = channel.get('StreamData', {}).get('HlsStreamUrl', '')
            logo = channel.get('PrimaryLogoImageUrl', '').strip()
            group = channel.get('Categories', [{}])[0].get('Name', 'Genel')
            
            if name and hls_url:
                m3u_content += f'#EXTINF:-1 tvg-id="{idx}" tvg-logo="{logo}" group-title="{group}",{name}\n'
                m3u_content += f'{hls_url}\n'
                kanal_sayisi += 1
        
        print(f"📺 {kanal_sayisi} geçerli kanal eklendi")
        return m3u_content
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

if __name__ == "__main__":
    result = get_canli_tv_m3u()
    if result:
        with open("tvheryerde.m3u", "w", encoding="utf-8") as f:
            f.write(result)
        print("✅ tvheryerde.m3u oluşturuldu")
    else:
        print("❌ M3U oluşturulamadı")