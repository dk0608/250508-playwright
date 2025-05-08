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
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_load_state("load", timeout=60000)  # ← 変更
        time.sleep(3)  # ← 保険として3秒待つ（任意で増減可）
        html = page.content()
        browser.close()

    return jsonify({"html": html})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
