from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# YouTube kanal kimliği — buraya kendi kanal ID’ni ekle
CHANNEL_ID = "UCxxxxxxxxxxxxxx"

@app.route('/')
def index():
    lives = get_live_videos(CHANNEL_ID)
    return render_template('index.html', lives=lives)

@app.route('/api/lives')
def api_lives():
    lives = get_live_videos(CHANNEL_ID)
    return jsonify(lives)

def get_live_videos(channel_id):
    """YouTube kanalında canlı yayın var mı diye kontrol eder."""
    url = f"https://www.youtube.com/channel/{channel_id}/live"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    lives = []
    for meta in soup.find_all("meta"):
        if meta.get("itemprop") == "name":
            title = meta.get("content")
        if meta.get("itemprop") == "url":
            live_url = "https://www.youtube.com" + meta.get("content")
            lives.append({"title": title, "url": live_url})
    return lives

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=False)
