from flask import Flask, render_template_string, request, redirect, url_for, Response
import re
import requests

app = Flask(__name__)

# --- CONFIGURATION (Change this to your actual ID later) ---
# Your Publisher ID looks like: pub-1234567890123456
ADSENSE_ID = "pub-0000000000000000" 

# --- STYLES ---
CSS = """
<style>
    :root { --primary: #ff0000; --dark: #0f0f0f; --card: #1e1e1e; --light: #ffffff; --gray: #aaaaaa; }
    body { font-family: 'Inter', sans-serif; background: var(--dark); color: var(--light); margin: 0; padding: 0; line-height: 1.7; }
    .nav { background: #000; padding: 20px 0; text-align: center; border-bottom: 3px solid var(--primary); position: sticky; top: 0; z-index: 1000; }
    .nav a { color: white; text-decoration: none; font-weight: bold; font-size: 24px; }
    
    /* AD SLOTS */
    .ad-slot { background: #1a1a1a; width: 100%; max-width: 728px; min-height: 90px; margin: 20px auto; border: 1px dashed #333; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    
    .main-wrapper { display: flex; flex-direction: column; align-items: center; width: 100%; padding: 20px; box-sizing: border-box; }
    .container { background: var(--card); padding: 40px; border-radius: 16px; width: 100%; max-width: 850px; text-align: center; box-sizing: border-box; margin-bottom: 30px; }
    .article-section { max-width: 850px; text-align: left; background: #151515; padding: 40px; border-radius: 16px; margin-top: 25px; border: 1px solid #222; }
    input { width: 100%; padding: 18px; border: 2px solid #333; border-radius: 12px; margin-bottom: 20px; box-sizing: border-box; font-size: 16px; background: #2a2a2a; color: white; outline: none; transition: 0.3s; }
    input:focus { border-color: var(--primary); box-shadow: 0 0 10px rgba(255,0,0,0.2); }
    .btn { background: var(--primary); color: white; border: none; padding: 18px 32px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 100%; font-size: 18px; transition: 0.2s; text-decoration: none; display: flex; justify-content: center; align-items: center; }
    .btn:hover { background: #cc0000; transform: translateY(-2px); }
    .btn-download { background: #2ba640; margin-top: 20px; }
    footer { margin-top: 50px; padding: 40px; text-align: center; color: var(--gray); font-size: 14px; border-top: 1px solid #222; width: 100%; }
    footer a { color: var(--gray); margin: 0 15px; text-decoration: none; }
    h2 { color: var(--primary); font-size: 28px; margin-bottom: 15px; }
    h3 { color: #eee; margin-top: 25px; }
    p { margin-bottom: 15px; color: #ccc; }
</style>
"""

# --- HTML TEMPLATE HELPER ---
def render_page(content, title):
    # This is the Google Ads script that goes in the <head>
    adsense_script = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-{ADSENSE_ID}" crossorigin="anonymous"></script>'
    
    # This is an example of an In-Feed or Display Ad Unit
    ad_unit_code = f"""
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-{ADSENSE_ID}"
         data-ad-slot="YOUR_AD_SLOT_ID_HERE"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script> (adsbygoogle = window.adsbygoogle || []).push({{}}); </script>
    """

    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>{{{{ title }}}} - GetYThumbnail</title>
        {adsense_script}
        {CSS}
    </head>
    <body>
        <div class='nav'><a href='/'>GETYTHUMBNAIL <span style='color:red'>PRO</span></a></div>
        
        <div class='ad-slot'>{ad_unit_code}</div>

        <div class='main-wrapper'>{content}</div>
        
        <div class='ad-slot'>{ad_unit_code}</div>

        <footer>
            <p>&copy; 2026 GetYThumbnail. All rights reserved.</p>
            <a href='/privacy'>Privacy Policy</a> | <a href='/contact'>Contact Us</a>
        </footer>
    </body>
    </html>
    """
    return render_template_string(full_html, title=title)

# --- LOGIC ---
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
        <p style="color:#888; margin-bottom:30px;">The fastest way to get high-quality YouTube video covers for free.</p>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste YouTube video link here..." required>
            <button type="submit" class="btn">GET THUMBNAIL NOW</button>
        </form>
    </div>

    <div class="article-section">
        <h2>Expert Guide: How to Download YouTube Thumbnails</h2>
        <p>Whether you are a graphic designer looking for inspiration or a content creator analyzing competitor strategies, our tool makes fetching video covers simple.</p>
        <ol>
            <li><strong>Copy URL:</strong> Navigate to the YouTube video and copy the link.</li>
            <li><strong>Process:</strong> Paste the link into the input field above.</li>
            <li><strong>Save:</strong> Click 'Download Full HD' to save the file.</li>
        </ol>
    </div>
    """
    return render_page(content, "Free High-Resolution Thumbnail Downloader")

@app.route('/result/<vid>')
def result(vid):
    content = f"""
    <div class="container">
        <img src="https://img.youtube.com/vi/{vid}/maxresdefault.jpg" style="width:100%; border-radius:12px; border:2px solid #333;">
        <a href="/download/{vid}" class="btn btn-download">DOWNLOAD FULL HD (1080p)</a>
        <a href="/" style="display:block; margin-top:20px; color:#aaa; text-decoration:none;">← Download Another</a>
    </div>
    """
    return render_page(content, "Your High-Resolution Download")

@app.route('/privacy')
def privacy():
    return render_page("<div class='container'><h1>Privacy Policy</h1><p>We use Google AdSense to serve ads. These ads use cookies to serve content based on your browsing history.</p></div>", "Privacy Policy")

@app.route('/contact')
def contact():
    return render_page("<div class='container'><h1>Contact Us</h1><p>Support: support@getythumbnail.com</p></div>", "Contact Us")

@app.route('/ads.txt')
def ads_txt():
    # REQUIRED BY GOOGLE
    return f"google.com, {ADSENSE_ID}, DIRECT, f08c47fec0942fa0"

@app.route('/download/<vid>')
def download_file(vid):
    img_url = f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
    r = requests.get(img_url)
    if r.status_code != 200:
        r = requests.get(f"https://img.youtube.com/vi/{vid}/hqdefault.jpg")
    return Response(r.content, headers={"Content-Disposition": f"attachment; filename=GetYThumbnail_{vid}.jpg", "Content-Type": "image/jpeg"})

if __name__ == '__main__':
    app.run()
