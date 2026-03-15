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

# Load CSS from style.css
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

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
