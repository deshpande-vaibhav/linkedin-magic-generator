import streamlit as st
import asyncio
import os
from ai_logic import generate_comment, generate_caption, analyze_media

# Page Configuration
st.set_page_config(
    page_title="LinkedIn Comment Magic | AI-Powered Engagement",
    page_icon="🪄",
    layout="centered"
)

# Custom Styling to match the local premium theme exactly
st.markdown("""
<style>
    /* 1. Reset and Global Background */
    #root, .stApp {
        background: #0f172a !important;
        background-attachment: fixed;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    }

    /* Hide Streamlit Header & Toolbar */
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    /* 2. Main Content Card (The Container) */
    .block-container {
        max-width: 900px !important;
        padding: 50px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important; /* Extremely subtle */
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3) !important;
        margin: 40px auto !important;
    }

    /* 3. Typography Fixes */
    h1 {
        color: #0a66c2 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-bottom: 5px !important;
    }
    
    .subtitle {
        color: #94a3b8 !important;
        text-align: center !important;
        margin-bottom: 30px !important;
        font-size: 1rem !important;
    }

    label p {
        color: #f8fafc !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
    }

    /* 4. Custom Tabs (Button Toggle Look) */
    .stTabs {
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.03) !important;
        padding: 6px !important;
        border-radius: 12px !important;
        border: none !important; /* Removed border */
        gap: 15px !important;
        margin-bottom: 30px !important;
        justify-content: center !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px !important;
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-weight: 700 !important;
        flex: 1 !important;
        border: none !important;
        padding: 0 20px !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0a66c2 !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(10, 102, 194, 0.3) !important;
    }
    div[data-baseweb="tab-highlight"] {
        display: none !important; /* Remove red underline */
    }

    /* 5. Input Fields (Aggressive Overrides) */
    .stTextArea textarea, .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background: rgba(43, 49, 65, 0.5) !important; /* Matched to dark grey in screenshot */
        color: #f8fafc !important;
        border: none !important; /* Removed white border */
        border-radius: 10px !important;
        padding: 12px 14px !important;
    }
    
    /* Subtle hover/focus to indicate interactivity without hard lines */
    .stTextArea textarea:focus, .stTextInput input:focus {
        background: rgba(53, 59, 75, 0.6) !important;
        box-shadow: 0 0 0 2px rgba(10, 102, 194, 0.3) !important;
    }

    /* 6. File Uploader (Dashed Box) */
    .stFileUploader section {
        background-color: transparent !important;
        border: 2px dashed rgba(255, 255, 255, 0.15) !important; /* Softer dashed line */
        border-radius: 12px !important;
        padding: 30px !important;
        color: #94a3b8 !important;
    }
    .stFileUploader section div[data-testid="stMarkdownContainer"] p {
        color: #94a3b8 !important;
    }

    /* 7. Divider (Manual OR) */
    .divider-or {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 700;
        margin: 20px 0;
        position: relative;
    }
    .divider-or::before, .divider-or::after {
        content: "";
        position: absolute;
        top: 50%;
        width: 45%;
        height: 1px;
        background: rgba(255, 255, 255, 0.05); /* Softer lines */
    }
    .divider-or::before { left: 0; }
    .divider-or::after { right: 0; }

    /* 8. Action Button */
    .stButton>button {
        width: 100% !important;
        background-color: #0a66c2 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-top: 20px !important;
        transition: all 0.3s ease !important;
        text-transform: none !important;
    }
    .stButton>button:hover {
        background-color: #004182 !important;
        transform: translateY(-2px) !important;
    }

    /* 9. Output Box */
    .output-box {
        background: rgba(25, 31, 44, 0.8) !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: none !important; /* Removed white border */
        margin-top: 40px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3) !important;
    }
    
    footer { display: none !important; }
    .footer {
        text-align: center;
        margin-top: 40px;
        font-size: 0.8rem;
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1>🪄 LinkedIn Comment Magic</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered engagement tailored to your style</p>', unsafe_allow_html=True)

# Check for API Key
from ai_logic import MISTRAL_API_KEY
if not MISTRAL_API_KEY:
    st.warning("Mistral API Key not found. Please add it to your environment variables or Streamlit secrets.")

tab1, tab2 = st.tabs(["Magic Comment Generator", "Magic Caption Generator"])

with tab1:
    post_caption = st.text_area("Post Caption", placeholder="Paste the LinkedIn post caption here...", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        post_link = st.text_input("Post Link (Optional)", placeholder="https://linkedin.com/posts/...")
    with col2:
        profile_link_comment = st.text_input("User Profile Link (Optional)", placeholder="https://linkedin.com/in/...", key="profile_comment")
    
    col3, col4 = st.columns(2)
    with col3:
        tone = st.selectbox("Comment Tone", ["Supportive", "Professional", "Funny", "Thoughtful", "Curious"])
    with col4:
        model_comment = st.selectbox("AI Model", ["mistral-large-latest", "mistral-small-latest"], format_func=lambda x: "Mistral Large (Smartest)" if "large" in x else "Mistral Small (Fastest)")

    if st.button("Generate Magic Comment"):
        if not post_caption:
            st.error("Please enter a post caption")
        else:
            with st.spinner("Analyzing and generating..."):
                comment = asyncio.run(generate_comment(post_caption, post_link, profile_link_comment, tone, model_comment))
                st.markdown(f'<div class="output-box"><h3>Generated Magic</h3><hr>{comment}</div>', unsafe_allow_html=True)

with tab2:
    thoughts = st.text_area("Your Thoughts / Topic", placeholder="What is this post about? Add your key messages here...", height=150)
    
    st.markdown("### Media (Image/Video)")
    media_file = st.file_uploader("Upload Image or Video", type=["jpg", "jpeg", "png", "webp", "mp4"])
    
    st.markdown('<div class="divider-or">OR</div>', unsafe_allow_html=True)
    
    media_url = st.text_input("Direct link to image/video", placeholder="Direct link to image/video (Drive, Cloud, etc.)")
    
    col1, col2 = st.columns(2)
    with col1:
        profile_link_caption = st.text_input("Your LinkedIn Profile Link", placeholder="https://linkedin.com/in/...", key="profile_caption")
    with col2:
        model_caption = st.selectbox("AI Model", ["mistral-large-latest", "mistral-small-latest"], format_func=lambda x: "Mistral Large (Smartest)" if "large" in x else "Mistral Small (Fastest)", key="model_caption")

    if st.button("Generate Magic Caption"):
        if not thoughts:
            st.error("Please enter your thoughts or a topic")
        else:
            with st.spinner("Analyzing media and generating caption..."):
                analyzed_media_desc = ""
                if media_file:
                    os.makedirs("temp_uploads", exist_ok=True)
                    temp_path = os.path.join("temp_uploads", media_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(media_file.getbuffer())
                    analyzed_media_desc = asyncio.run(analyze_media(file_path=temp_path))
                    os.remove(temp_path)
                elif media_url:
                    analyzed_media_desc = asyncio.run(analyze_media(media_url=media_url))
                
                caption = asyncio.run(generate_caption(thoughts, profile_link_caption, analyzed_media_desc, model_caption))
                st.markdown(f'<div class="output-box"><h3>Generated Magic</h3><hr>{caption}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">© 2026 LinkedIn Comment Magic. Powered by Mistral AI.</div>', unsafe_allow_html=True)
