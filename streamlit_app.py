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

# Custom Styling to match the premium theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        background-color: #0a66c2;
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #004182;
        transform: translateY(-2px);
    }
    .output-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

st.title("🪄 LinkedIn Comment Magic")
st.markdown("AI-powered engagement tailored to your style")

# Check for API Key
from ai_logic import MISTRAL_API_KEY
if not MISTRAL_API_KEY:
    st.warning("Mistral API Key not found. Please add it to your environment variables or Streamlit secrets.")
    st.info("To add secrets in Streamlit Cloud: Settings -> Secrets -> Add MISTRAL_API_KEY=your_key")

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
                st.subheader("Generated Magic")
                st.markdown(f'<div class="output-box">{comment}</div>', unsafe_allow_html=True)
                if st.button("Copy to Clipboard", key="copy_comment"):
                    st.write("Copied! (Note: Streamlit copy depends on browser context)")

with tab2:
    thoughts = st.text_area("Your Thoughts / Topic", placeholder="What is this post about? Add your key messages here...", height=150)
    
    st.markdown("### Media (Image/Video)")
    media_file = st.file_uploader("Upload Image or Video", type=["jpg", "jpeg", "png", "webp", "mp4"])
    media_url = st.text_input("OR Direct link to image/video", placeholder="Direct link to image/video (Drive, Cloud, etc.)")
    
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
                    # Save temp file
                    os.makedirs("temp_uploads", exist_ok=True)
                    temp_path = os.path.join("temp_uploads", media_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(media_file.getbuffer())
                    
                    analyzed_media_desc = asyncio.run(analyze_media(file_path=temp_path))
                    os.remove(temp_path)
                elif media_url:
                    analyzed_media_desc = asyncio.run(analyze_media(media_url=media_url))
                
                caption = asyncio.run(generate_caption(thoughts, profile_link_caption, analyzed_media_desc, model_caption))
                st.subheader("Generated Magic")
                st.markdown(f'<div class="output-box">{caption}</div>', unsafe_allow_html=True)

st.divider()
st.markdown("© 2026 LinkedIn Comment Magic. Powered by Mistral AI.")
