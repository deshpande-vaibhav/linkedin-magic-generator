import streamlit as st
import asyncio
from ai_logic import generate_comment, generate_caption, analyze_media
import os

# 1. Page Configuration
st.set_page_config(
    page_title="LinkedIn Comment Magic | AI-Powered Engagement",
    page_icon="🪄",
    layout="centered"
)

# 1. Page Configuration
st.set_page_config(
    page_title="LinkedIn Comment Magic | AI-Powered Engagement",
    page_icon="🪄",
    layout="centered"
)

# 2. Extreme CSS Overrides for Unified Look
st.markdown("""
<style>
    /* 1. Global Reset */
    #root, .stApp {
        background: #0f172a !important;
        background-attachment: fixed;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    }
    
    /* Remove padding and headers */
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    
    /* Unified Card System */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 850px !important;
    }

    /* Target the main container specifically */
    [data-testid="stVerticalBlock"] > div:has(.premium-card) {
        padding: 0 !important;
    }

    .premium-card {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5) !important;
        padding: 40px !important;
        margin-bottom: 30px !important;
    }

    /* 3. Typography */
    h1 {
        color: #3b82f6 !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-bottom: 15px !important;
        letter-spacing: -0.5px !important;
    }
    .subtitle {
        color: #94a3b8 !important;
        text-align: center !important;
        margin-bottom: 40px !important;
        font-size: 1.1rem !important;
    }

    /* 4. Pill Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(15, 23, 42, 0.4) !important;
        padding: 6px !important;
        border-radius: 50px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        gap: 10px !important;
        margin-bottom: 40px !important;
        display: flex !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        color: #94a3b8 !important;
        font-weight: 700 !important;
        flex: 1 !important;
        height: 44px !important;
        border-radius: 40px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3) !important;
    }
    div[data-baseweb="tab-highlight"] { display: none !important; }
    div[data-baseweb="tab-border"] { display: none !important; }

    /* 5. Inputs (Dark & Premium) */
    .stTextArea textarea, .stTextInput input, div[data-baseweb="select"] {
        background: rgba(15, 23, 42, 0.5) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #3b82f6 !important;
        background: rgba(15, 23, 42, 0.7) !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
    }
    
    label p {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        margin-bottom: 10px !important;
    }

    /* 6. Action Button */
    .stButton>button {
        width: 100% !important;
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.2) !important;
    }
    .stButton>button:hover {
        background: #2563eb !important;
        transform: translateY(-2px);
        box-shadow: 0 15px 25px rgba(59, 130, 246, 0.3) !important;
    }

    /* 7. Output Box */
    .output-box {
        margin-top: 30px !important;
        padding: 30px !important;
        background: rgba(15, 23, 42, 0.4) !important;
        border-radius: 18px !important;
        border: 1.5px solid #3b82f6 !important;
        color: #f8fafc !important;
    }
    
    footer { display: none !important; }
    .footer {
        text-align: center;
        margin-top: 20px;
        font-size: 0.85rem;
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)

# 3. Main Application Container
with st.container():
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    
    # Header & Subtitle (Inside the card)
    st.markdown('<h1>🪄 LinkedIn Comment Magic</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-powered engagement tailored to your style</p>', unsafe_allow_html=True)

    # Tabs (Inside the card)
    tab1, tab2 = st.tabs(["Magic Comment Generator", "Magic Caption Generator"])

    # --- Magic Comment Generator ---
    with tab1:
        post_caption = st.text_area("Post Caption", placeholder="Paste the LinkedIn post caption here...", height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            post_link = st.text_input("Post Link (Optional)", placeholder="https://linkedin.com/posts/...")
        with col2:
            profile_link_comment = st.text_input("User Profile Link (Optional)", placeholder="https://linkedin.com/in/...")
        
        col3, col4 = st.columns(2)
        with col3:
            tone = st.selectbox("Comment Tone", ["Supportive", "Professional", "Insightful", "Casual", "Funny", "Questioning"])
        with col4:
            model_comment = st.selectbox("AI Model", ["Mistral Large (Smartest)", "Mistral Small (Fastest)"], key="model_com")

        if st.button("Generate Magic Comment"):
            if not post_caption:
                st.warning("Please enter a post caption")
            else:
                with st.spinner("Generating magic..."):
                    selected_model = "mistral-large-latest" if "Large" in model_comment else "mistral-small-latest"
                    comment = asyncio.run(generate_comment(post_caption, post_link, profile_link_comment, tone, selected_model))
                    st.markdown(f'<div class="output-box"><h3>Magic Comment Generated</h3>{comment}</div>', unsafe_allow_html=True)

    # --- Magic Caption Generator ---
    with tab2:
        user_thoughts = st.text_area("Your Thoughts / Topic", placeholder="What is this post about? Add your key messages here...", height=150)
        
        st.markdown('<label>Media (Image/Video)</label>', unsafe_allow_html=True)
        media_file = st.file_uploader("Upload Image or Video", type=["jpg", "jpeg", "png", "webp", "mp4", "mpeg"], label_visibility="collapsed")
        
        st.markdown('<div style="text-align:center; color:#94a3b8; font-size:0.9rem; margin:15px 0; font-weight:700;">OR</div>', unsafe_allow_html=True)
        
        media_url = st.text_input("Direct link to image/video", placeholder="Drive, Cloud, etc.")
        
        col1, col2 = st.columns(2)
        with col1:
            profile_link_caption = st.text_input("Your LinkedIn Profile Link", placeholder="https://linkedin.com/in/...", key="prof_cap")
        with col2:
            model_caption = st.selectbox("AI Model", ["Mistral Large (Smartest)", "Mistral Small (Fastest)"], key="model_cap")

        if st.button("Generate Magic Caption"):
            if not user_thoughts:
                st.warning("Please enter your thoughts or a topic")
            else:
                with st.spinner("Analyzing media & generating caption..."):
                    selected_model = "mistral-large-latest" if "Large" in model_caption else "mistral-small-latest"
                    
                    analyzed_desc = ""
                    if media_file:
                        temp_path = f"temp_{media_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(media_file.getbuffer())
                        analyzed_desc = asyncio.run(analyze_media(file_path=temp_path))
                        os.remove(temp_path)
                    elif media_url:
                        analyzed_desc = asyncio.run(analyze_media(media_url=media_url))
                    
                    caption = asyncio.run(generate_caption(user_thoughts, profile_link_caption, analyzed_desc, selected_model))
                    st.markdown(f'<div class="output-box"><h3>Magic Caption Generated</h3>{caption}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Close premium-card

st.markdown('<div class="footer">© 2026 LinkedIn Comment Magic. Powered by Mistral AI.</div>', unsafe_allow_html=True)
