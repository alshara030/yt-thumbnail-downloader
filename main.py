from flask import Flask, render_template, request, redirect, url_for, Response
import re
import requests

app = Flask(__name__)

# REPLACE THIS with your actual ID from Google
ADSENSE_ID = "pub-1935984181885001"

def extract_id(url):
    match = re.search(r"(?:v=|\/|be\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_id = extract_id(request.form.get('url'))
        if video_id: 
            return redirect(url_for('result', vid=video_id))
    return render_template('index.html', adsense_id=ADSENSE_ID)

@app.route('/result/<vid>')
def result(vid):
    return render_template('result.html', vid=vid, adsense_id=ADSENSE_ID)

@app.route('/ads.txt')
def ads_txt():
    return f"google.com, {ADSENSE_ID}, DIRECT, f08c47fec0942fa0"

@app.route('/download/<vid>')
def download_file(vid):
    img_url = f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
    r = requests.get(img_url)
    if r.status_code != 200:
        r = requests.get(f"https://img.youtube.com/vi/{vid}/hqdefault.jpg")
    return Response(r.content, headers={
        "Content-Disposition": f"attachment; filename=GetYThumbnail_{vid}.jpg",
        "Content-Type": "image/jpeg"
    })

if __name__ == '__main__':
    app.run()
