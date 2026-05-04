import streamlit as st
import tempfile
import subprocess
import os

# Serve ads.txt manually
query = st.query_params

if "ads.txt" in st.query_params:
    st.text("google.com, pub-4586891706711357, DIRECT, f08c47fec0942fa0")
    st.stop()
st.set_page_config(page_title="Media Converter - Convert Files Online", layout="wide")

# 🔥 REMOVE DEFAULT STREAMLIT UI
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
header {visibility:hidden;}
footer {visibility:hidden;}
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
    padding-left: 60px !important;
    padding-right: 60px !important;}
main {padding: 0 !important;}
</style>
""", unsafe_allow_html=True)

# 🎨 COMPREHENSIVE STYLING - FREECONVERT STYLE
st.markdown("""
<style>
* {margin:0; padding:0; box-sizing:border-box;}

body {background-color:#fff; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;}

.navbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:20px 60px;
    background:white;
    border-bottom:1px solid #f0f0f0;
    box-shadow:0 1px 3px rgba(0,0,0,0.05);
    width:100%;
    margin-left:0;
}

.logo {font-weight:700; font-size:20px; color:#2e7d32;}

.navbar-links {display:flex; gap:30px; font-size:14px;}

.navbar-links span {color:#666; cursor:pointer;}

.navbar-right {display:flex; gap:20px; align-items:center;}

.hero {
    text-align:center;
    padding:60px 60px;
    background:white;
    border-bottom:1px solid #f0f0f0;
    width:100%;
    margin-left:0;
}

.hero h1 {font-size:48px; color:#1a1a1a; margin-bottom:15px; font-weight:700;}

.hero p {font-size:18px; color:#666; margin-bottom:30px;}

.container {max-width:100%; margin:0; padding:0 60px; width:100%;}

.tabs-container {margin:40px 0;}

.input-section {
    background:white;
    border:2px dashed #ddd;
    border-radius:8px;
    padding:40px;
    text-align:center;
    margin:30px 0;
}

.file-input-wrapper {
    display:flex;
    flex-direction:column;
    gap:20px;
}

.controls-row {
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    gap:20px;
    margin:20px 0;
}

.format-select {
    padding:12px 16px;
    border:1px solid #ddd;
    border-radius:6px;
    font-size:14px;
    background:white;
}

.convert-btn {
    background:#5e6eff;
    color:white;
    border:none;
    padding:14px 40px;
    border-radius:6px;
    font-size:16px;
    font-weight:600;
    cursor:pointer;
    transition:background 0.3s;
    width:100%;
}

.convert-btn:hover {background:#4a57d4;}

.info-section {
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    gap:40px;
    margin:60px 0;
    padding:40px 0;
}

.info-card {
    text-align:center;
}

.info-icon {font-size:48px; margin-bottom:20px;}

.info-card h3 {font-size:20px; color:#1a1a1a; margin-bottom:15px; font-weight:600;}

.info-card p {color:#666; line-height:1.6; font-size:14px;}

.footer {
    background:#2a3f5f;
    color:#fff;
    padding:60px;
    margin-top:80px;
}

.footer-content {max-width:1200px; margin:0 auto;}

.footer-grid {
    display:grid;
    grid-template-columns:repeat(6, 1fr);
    gap:40px;
    margin-bottom:40px;
}

.footer-column h4 {font-size:16px; margin-bottom:20px; font-weight:600;}

.footer-column a {
    display:block;
    color:#b0b8c1;
    text-decoration:none;
    font-size:14px;
    margin-bottom:12px;
    cursor:pointer;
    transition:color 0.3s;
}

.footer-column a:hover {color:white;}

.footer-bottom {
    border-top:1px solid #3a4d63;
    padding-top:30px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.footer-bottom p {font-size:12px; color:#b0b8c1;}

.ad-space {
    background:#f5f5f5;
    border:2px dashed #ddd;
    border-radius:8px;
    padding:40px;
    text-align:center;
    color:#999;
    margin:40px 0;
    font-size:14px;
}

.stTabs {margin-top:20px;}

.upload-label {font-size:14px; color:#666; margin-bottom:10px; display:block; text-align:left;}

.success-message {
    background:#d4edda;
    border:1px solid #c3e6cb;
    color:#155724;
    padding:15px 20px;
    border-radius:6px;
    margin:20px 0;
}

.error-message {
    background:#f8d7da;
    border:1px solid #f5c6cb;
    color:#721c24;
    padding:15px 20px;
    border-radius:6px;
    margin:20px 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "current_tab" not in st.session_state:
    st.session_state.current_tab = 0

# Format definitions
formats_data = {
    "audio": {
        "icon": "🎵",
        "title": "Audio Converter",
        "description": "Convert audio files to MP3, WAV, FLAC, AAC, OGG, M4A, WMA, OPUS, and more formats.",
        "formats": ["mp3", "wav", "flac", "aac", "ogg", "m4a", "wma", "opus", "aif", "aiff"]
    },
    "video": {
        "icon": "🎬",
        "title": "Video Converter",
        "description": "Convert video files to MP4, AVI, MKV, MOV, WMV, FLV, WEBM, M4V, 3GP, and more.",
        "formats": ["mp4", "avi", "mkv", "mov", "wmv", "flv", "webm", "m4v", "3gp", "mpg"]
    },
    "image": {
        "icon": "🖼️",
        "title": "Image Converter",
        "description": "Convert images to JPG, PNG, BMP, GIF, WEBP, SVG, TIFF formats.",
        "formats": ["jpg", "jpeg", "png", "bmp", "tiff", "gif", "webp", "svg"]
    },
    "document": {
        "icon": "📄",
        "title": "Document Converter",
        "description": "Convert documents between PDF, DOCX, TXT, RTF formats.",
        "formats": ["pdf", "docx", "txt", "rtf"]
    },
    "archive": {
        "icon": "📦",
        "title": "Archive Converter",
        "description": "Create and convert archive files to ZIP, RAR, 7Z, TAR, GZ formats.",
        "formats": ["zip", "rar", "7z", "tar", "gz"]
    },
    "ebook": {
        "icon": "📕",
        "title": "Ebook Converter",
        "description": "Convert ebook formats EPUB, MOBI, AZW, and PDF.",
        "formats": ["epub", "mobi", "azw", "pdf"]
    }
}

# Helper function
def convert_file(input_path, output_format, category):
    output_path = input_path + f".{output_format}"
    try:
        if category == "audio":
            cmd = ["ffmpeg", "-i", input_path, "-q:a", "0", "-map", "a", output_path]
        else:
            cmd = ["ffmpeg", "-i", input_path, output_path]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.exists(output_path):
            return output_path
        return None
    except Exception as e:
        return None

# NAVBAR
st.markdown("""
<div class="navbar">
    <div class="logo">File Converter</div>
    <div class="navbar-links">
        <span>All Tools</span>
        <span>Pricing</span>
        <span>Help</span>
    </div>
</div>
""", unsafe_allow_html=True)

# HERO SECTION
# st.markdown("""
# <div class="hero">
#     <h1>File Converter</h1>
#     <p>Easily convert files from one format to another, online.</p>
# </div>
# """, unsafe_allow_html=True)

# MAIN CONTAINER
# st.markdown('<div class="container">', unsafe_allow_html=True)

# AD SPACE
st.markdown('<div class="ad-space">Advertisement Space</div>', unsafe_allow_html=True)

# TABS
tab_names = [f"{info['icon']} {info['title']}" for info in formats_data.values()]
tabs = st.tabs(tab_names)

tab_keys = list(formats_data.keys())

for idx, tab in enumerate(tabs):
    with tab:
        card_key = tab_keys[idx]
        card_info = formats_data[card_key]
        
        # File upload section
        # st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown('<label class="upload-label">Choose File:</label>', unsafe_allow_html=True)
            uploaded = st.file_uploader(
                f"Upload {card_key}",
                type=card_info['formats'],
                key=f"upload_{card_key}_{idx}",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown('<label class="upload-label">Output Format:</label>', unsafe_allow_html=True)
            to_format = st.selectbox(
                "Output",
                card_info['formats'],
                key=f"to_{card_key}_{idx}",
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown('<label class="upload-label">Convert:</label>', unsafe_allow_html=True)
            if st.button("🔄 Convert", key=f"btn_{card_key}_{idx}", use_container_width=True):
                if uploaded:
                    with tempfile.NamedTemporaryFile(delete=False) as tmp:
                        tmp.write(uploaded.read())
                        input_path = tmp.name
                    
                    output_path = convert_file(input_path, to_format, card_key)
                    
                    if output_path:
                        with open(output_path, "rb") as f:
                            file_data = f.read()
                        
                        st.session_state[f"converted_{card_key}"] = file_data
                        st.session_state[f"converted_name_{card_key}"] = f"converted.{to_format}"
                        st.markdown('<div class="success-message">✅ Conversion complete!</div>', unsafe_allow_html=True)
                        
                        os.remove(input_path)
                        os.remove(output_path)
                    else:
                        st.markdown('<div class="error-message">❌ Conversion failed. Try another format.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">⚠️ Please upload a file first.</div>', unsafe_allow_html=True)
        
        # Download button
        if f"converted_{card_key}" in st.session_state:
            st.download_button(
                f"📥 Download {to_format.upper()}",
                st.session_state[f"converted_{card_key}"],
                file_name=st.session_state[f"converted_name_{card_key}"],
                key=f"download_{card_key}_{idx}",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Description
        st.markdown(f"**{card_info['description']}**")

# AD SPACE 2
st.markdown('<div class="ad-space">📢 Advertisement Space</div>', unsafe_allow_html=True)

# INFO SECTION
st.markdown("""
<div class="info-section">
    <div class="info-card">
        <div class="info-icon">📁</div>
        <h3>Convert Any File</h3>
        <p>Supports 1500+ file format conversions. Convert videos, audio, images, documents, archives and more.</p>
    </div>
    <div class="info-card">
        <div class="info-icon">☁️</div>
        <h3>Works Anywhere</h3>
        <p>Convert files online from Windows, Mac, Linux, or any device. No software installation needed.</p>
    </div>
    <div class="info-card">
        <div class="info-icon">🔒</div>
        <h3>Privacy Guaranteed</h3>
        <p>Files are processed securely with SSL encryption. Automatically deleted after conversion.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <div class="footer-grid">
            <div class="footer-column">
                <h4>Audio Converter</h4>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(1)').click()">MP3 Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(1)').click()">WAV Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(1)').click()">AAC Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(1)').click()">Audio Converter</a>
            </div>
            <div class="footer-column">
                <h4>Video Converter</h4>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(2)').click()">MP4 Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(2)').click()">AVI Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(2)').click()">MKV Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(2)').click()">Video Converter</a>
            </div>
            <div class="footer-column">
                <h4>Image Converter</h4>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(3)').click()">JPG to PNG</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(3)').click()">PNG Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(3)').click()">GIF Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(3)').click()">Image Converter</a>
            </div>
            <div class="footer-column">
                <h4>Document Converter</h4>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(4)').click()">PDF Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(4)').click()">DOCX Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(4)').click()">TXT Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(4)').click()">Document Converter</a>
            </div>
            <div class="footer-column">
                <h4>Archive Converter</h4>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(5)').click()">ZIP Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(5)').click()">RAR Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(5)').click()">7Z Converter</a>
                <a onclick="document.querySelector('[role=tablist] > [role=tab]:nth-child(5)').click()">Archive Converter</a>
            </div>
            <div class="footer-column">
                <h4>Resources</h4>
                <a>About Us</a>
                <a>Blog</a>
                <a>Privacy</a>
                <a>Contact</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2026 Media Converter. All rights reserved.</p>
            <p style="text-align:right;">Made with ❤️</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
