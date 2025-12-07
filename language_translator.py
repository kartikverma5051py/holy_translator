import streamlit as st
import json
from deep_translator import GoogleTranslator
import base64

st.set_page_config(page_title="Holy Translator", layout="centered")

# ================= Local background image =================
image_path = "WhatsApp_Image.jpeg"

# Read and encode image
with open(image_path, "rb") as f:
    img_bytes = f.read()

encoded_bg = base64.b64encode(img_bytes).decode()

# Inject CSS for Streamlit background
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/png;base64,{encoded_bg}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
.block-container {{
    background: rgba(0,0,0,0.55);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(4px);
}}
label, h1, h2, h3, p, span {{
    color: white !important;
}}
</style>
""", unsafe_allow_html=True)

# ================= UI =================
st.title("✝ Holy Translator")

uploaded = st.file_uploader("📄 Upload a TXT file", type=["txt"])

if uploaded:
    text = uploaded.read().decode("utf-8")
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    st.info("🌍 Auto-detecting language → Translating to English")

    if st.button("✨ Translate Now"):
        output = []
        for line in lines:
            translated = GoogleTranslator(source="auto", target="en").translate(line)
            output.append((line, translated))

        st.success("✅ Translation completed!")

        # ================= Download TXT =================
        final_text = "\n\n".join([f"{e}\n{h}" for e, h in output])
        b64 = base64.b64encode(final_text.encode()).decode()
        href = f'<a download="translated.txt" href="data:text/plain;base64,{b64}">📥 Download Result</a>'
        st.markdown(href, unsafe_allow_html=True)

        # ================= Slideshow =================
        slides = json.dumps([{"eng": e, "tr": h} for e, h in output])

        html_template = f"""
<!DOCTYPE html>
<html>
<head>
<title>Holy Slideshow</title>

<style>
    body {{
        background-image: url("data:image/png;base64,{encoded_bg}");
        background-size: cover;
        background-repeat: no-repeat;
        font-family: Arial;
        color: white;
        text-align: center;
        overflow: hidden;
    }}
    #slide-box {{
        margin-top: 22vh;
        font-size: 68px;
        line-height: 1.5;
        white-space: pre-wrap;
        color: white;
        font-weight: 900;
    }}
    #controls {{
        position: fixed;
        bottom: 30px;
        width: 100%;
        text-align: center;
    }}
    button {{
        padding: 14px 28px;
        font-size: 22px;
        border-radius: 12px;
        border: none;
        margin: 10px;
        cursor: pointer;
    }}
</style>

<script>
let slides = {slides};
let idx = 0;
let autoSlide = true;
let slideInterval;

function render(i){{
    const box = document.getElementById("slide-box");
    box.innerHTML = slides[i].eng + "<br><br>" + slides[i].tr;
}}

function nextSlide(){{
    idx = (idx + 1) < slides.length ? idx + 1 : idx;
    render(idx);
}}

function prevSlide(){{
    idx = (idx - 1) >= 0 ? idx - 1 : 0;
    render(idx);
}}

function startAuto(){{
    slideInterval = setInterval(nextSlide, 2000);
}}

function stopAuto(){{
    clearInterval(slideInterval);
}}

document.addEventListener("keydown", function(event){{
    if(event.key === "ArrowRight") nextSlide();
    if(event.key === "ArrowLeft") prevSlide();
    if(event.key === " ") {{
        autoSlide = !autoSlide;
        if(autoSlide) startAuto();
        else stopAuto();
    }}
    if(event.key === "Escape"){{
        document.getElementById("controls").style.display = "none";
    }}
}});

window.onload = function(){{
    render(0);
    startAuto();
}};
</script>

</head>
<body>
<div id="slide-box"></div>
<div id="controls">
    <button onclick="prevSlide()">Prev</button>
    <button onclick="nextSlide()">Next</button>
</div>
</body>
</html>
"""

        # Convert HTML to base64 for new tab
        b64_html = base64.b64encode(html_template.encode()).decode()
        slideshow_link = f"""
        <a href="data:text/html;base64,{b64_html}" target="_blank"
           style="color: yellow; font-size: 22px;">
           🌐 OPEN FULLSCREEN SLIDESHOW (NEW TAB)
        </a>
        """
        st.markdown(slideshow_link, unsafe_allow_html=True)
