from flask import Flask, render_template_string, request, redirect, url_for, Response
import re
import requests

app = Flask(__name__)

# --- STYLES ---
CSS = """
<style>
    :root { --primary: #ff0000; --dark: #0f0f0f; --card: #1e1e1e; --light: #ffffff; --gray: #aaaaaa; }
    body { font-family: 'Inter', -apple-system, sans-serif; background: var(--dark); color: var(--light); margin: 0; padding: 0; line-height: 1.6; }
    .nav { background: #000; padding: 20px 0; text-align: center; border-bottom: 3px solid var(--primary); position: sticky; top: 0; z-index: 1000; }
    .nav a { color: white; text-decoration: none; font-weight: bold; font-size: 24px; }
    .ad-slot { background: #1a1a1a; width: 100%; max-width: 728px; min-height: 90px; margin: 20px auto; border: 1px dashed #333; display: flex; align-items: center; justify-content: center; color: #444; font-size: 12px; }
    .main-wrapper { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 20px; box-sizing: border-box; }
    .container { background: var(--card); padding: 40px; border-radius: 16px; width: 100%; max-width: 800px; text-align: center; box-sizing: border-box; margin-bottom: 30px; }
    .info-section { max-width: 800px; text-align: left; background: #151515; padding: 30px; border-radius: 16px; margin-top: 20px; border: 1px solid #222; }
    input { width: 100%; padding: 16px; border: 2px solid #333; border-radius: 12px; margin-bottom: 20px; box-sizing: border-box; font-size: 16px; background: #2a2a2a; color: white; outline: none; }
    input:focus { border-color: var(--primary); }
    .btn { background: var(--primary); color: white; border: none; padding: 16px 32px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 100%; font-size: 18px; transition: 0.2s; text-decoration: none; display: flex; justify-content: center; align-items: center; }
    .btn:hover { background: #cc0000; transform: translateY(-2px); }
    .btn-download { background: #2ba640; margin-top: 20px; }
    .thumb-preview { width: 100%; border-radius: 12px; margin-bottom: 10px; border: 2px solid #333; }
    footer { margin-top: 50px; padding: 30px; text-align: center; color: var(--gray); font-size: 14px; border-top: 1px solid #222; width: 100%; }
    footer a { color: var(--gray); margin: 0 10px; text-decoration: none; }
    h2 { color: var(--primary); margin-top: 0; }
    li { margin-bottom: 10px; }
</style>
"""

def render_page(content, title, vid=None):
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ title }} - GetYThumbnail</title>
        {CSS}
    </head>
    <body>
        <div class="nav"><a href="/">GETYTHUMBNAIL <span style="color:red">PRO</span></a></div>
        <div class="ad-slot">AD_CODE_TOP</div>
        <div class="main-wrapper">{content}</div>
        <div class="ad-slot">AD_CODE_BOTTOM</div>
        <footer>
            <p>&copy; 2026 GetYThumbnail. All rights reserved.</p>
            <a href="/privacy">Privacy Policy</a> | <a href="/contact">Contact Us</a>
        </footer>
    </body>
    </html>
    """
    return render_template_string(full_html, title=title, vid=vid)

def extract_id(url):
    match = re.search(r"(?:v=|\/|be\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_id = extract_id(request.form.get('url'))
        if video_id: return redirect(url_for('result', vid=video_id))
    
    content = """
    <div class="container">
        <h1>YouTube Thumbnail Downloader</h1>
        <p style="color:#888; margin-bottom:30px;">Download high-quality video covers for free.</p>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste YouTube link here..." required>
            <button type="submit" class="btn">GET THUMBNAIL</button>
        </form>
    </div>

    <div class="info-section">
        <h2>How to Use GetYThumbnail</h2>
        <ol>
            <li><strong>Copy the URL:</strong> Go to YouTube and copy the link of the video you want.</li>
            <li><strong>Paste the Link:</strong> Paste the URL into the search box above.</li>
            <li><strong>Download:</strong> Click "Get Thumbnail" and then click the green button to save the HD image.</li>
        </ol>
    </div>

    <div class="info-section">
        <h2>Why Use Our Tool?</h2>
        <p>GetYThumbnail is a professional, web-based tool designed for creators, designers, and researchers. We provide:</p>
        <ul>
            <li><strong>Full HD Quality:</strong> We always fetch the 1080p or 720p MaxRes version if available.</li>
            <li><strong>Fast & Free:</strong> No registration, no payments, and no software installation required.</li>
            <li><strong>Privacy First:</strong> We do not track your downloads or store your URLs on our server.</li>
        </ul>
    </div>
    """
    return render_page(content, "Free HD Thumbnail Downloader")

@app.route('/result/<vid>')
def result(vid):
    content = f"""
    <div class="container">
        <img src="https://img.youtube.com/vi/{vid}/maxresdefault.jpg" class="thumb-preview">
        <a href="/download/{vid}" class="btn btn-download">DOWNLOAD FULL HD</a>
        <a href="/" style="display:block; margin-top:20px; color:#aaa; text-decoration:none;">← Download another</a>
    </div>
    <div class="info-section">
        <h3>About your download</h3>
        <p>This image is the "MaxResDefault" version provided by YouTube's servers. If the image appears blurry, it may be because the original uploader did not provide a high-resolution thumbnail.</p>
    </div>
    """
    return render_page(content, "Your Download", vid=vid)

@app.route('/privacy')
def privacy():
    content = """<div class="container" style="text-align:left;"><h1>Privacy Policy</h1><p>Welcome to GetYThumbnail. We prioritize your privacy. We do not store personal data or the URLs you paste. Our service acts as a real-time bridge to YouTube's publicly available thumbnail images. We use Google AdSense to serve ads, which may use cookies to personalize content.</p></div>"""
    return render_page(content, "Privacy Policy")

@app.route('/contact')
def contact():
    content = """<div class="container"><h1>Contact Us</h1><p>Have issues or feedback? Contact us at: <strong>support@getythumbnail.com</strong></p></div>"""
    return render_page(content, "Contact Us")

@app.route('/download/<vid>')
def download_file(vid):
    img_url = f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
    try:
        r = requests.get(img_url)
        if r.status_code != 200:
            r = requests.get(f"https://img.youtube.com/vi/{vid}/hqdefault.jpg")
        return Response(r.content, headers={"Content-Disposition": f"attachment; filename=YT_Thumbnail_{vid}.jpg", "Content-Type": "image/jpeg"})
    except: return "Error", 404

if __name__ == '__main__':
    app.run(debug=True)