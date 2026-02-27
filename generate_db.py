import os
import csv
import time
import requests
from bs4 import BeautifulSoup

# --- 設定 ---
TARGET_DIR = "./contents"  # ここに動画ファイルを置いてください
OUTPUT_CSV = "dmm_library.csv"
WAIT_TIME = 1.5  # 検索エンジンへの負荷軽減

def extract_id(filename):
    name = os.path.splitext(filename)[0].lower()

    # ★ hhb で終わる特殊ケース
    if name.endswith("hhb"):
        return name[:-3]

    # 従来ロジック
    if '_' in name:
        name = name.split('_')[0]

    if name.endswith('2d'):
        name = name[:-2]

    return name

def get_title_via_duckduckgo(cid):
    """DuckDuckGoを使用してタイトルを検索取得する"""
    search_url = f"https://duckduckgo.com/html/?q=site:dmm.co.jp+{cid}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 最初の検索結果のリンクテキストを取得
        result = soup.find('a', class_='result__a')
        if result:
            title = result.get_text()
            # 「 - 動画 - FANZA」などの不要な部分をカット
            clean_title = title.split(' - ')[0].replace('FANZA', '').strip()
            return clean_title
        return "Title Not Found"
    except Exception:
        return "Search Error"

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"Error: {TARGET_DIR} が見つかりません。")
        return

    # 再帰的にファイルを取得
    all_files = []
    for dirpath, dirnames, filenames in os.walk(TARGET_DIR):
        for filename in filenames:
            full_path_actual = os.path.join(dirpath, filename)
            all_files.append(full_path_actual)
    
    print(f"{len(all_files)} 件のファイルを処理します...")

    with open(OUTPUT_CSV, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ファイル名', 'ID', 'タイトル', 'サムネURL', 'フルパス', 'CID推定方式'])

        for full_path_actual in all_files:
            filename = os.path.basename(full_path_actual)
            cid = extract_id(filename)
            full_path = os.path.abspath(full_path_actual)
            
            # サムネイルURLを予測生成（リクエストを飛ばさず文字列結合のみ）
            thumb_url = f"https://pics.dmm.co.jp/digital/video/{cid}/{cid}pl.jpg"
            
            # タイトルのみ外部検索
            print(f"Searching Title for: {cid}...")
            title = get_title_via_duckduckgo(cid)
            
            writer.writerow([filename, cid, title, thumb_url, full_path, 'fallback'])
            
            # 検索エンジンに怪しまれないためのウェイト
            time.sleep(WAIT_TIME)

    print(f"\n完了！ '{OUTPUT_CSV}' が生成されました。")

if __name__ == "__main__":
    main()