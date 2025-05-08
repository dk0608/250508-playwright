from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import time

app = Flask(__name__)

@app.route("/fetch-html", methods=["POST"])
def fetch_html():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    with sync_playwright() as p:
        # Cloudflare対策：UIあり、ステルスオプション追加
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        # Cloudflare対策：実ブラウザ風のUser-Agentを指定
        page = browser.new_page(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ))
        page.goto(url, timeout=60000)
        page.wait_for_load_state("load", timeout=60000)
        time.sleep(5)  # JS実行やCloudflare認証の待機時間として重要
        html = page.content()
        browser.close()

    return jsonify({"html": html})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
