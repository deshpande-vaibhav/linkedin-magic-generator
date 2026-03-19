import os
import httpx
import base64
from bs4 import BeautifulSoup
from mistralai.client import Mistral # Correct import for SDK v2.0.2
from dotenv import load_dotenv

load_dotenv()

def get_mistral_api_key():
    # 1. Try environment variable
    key = os.getenv("MISTRAL_API_KEY")
    if key:
        return key
    
    # 2. Try Streamlit secrets (for deployment)
    try:
        import streamlit as st
        if "MISTRAL_API_KEY" in st.secrets:
            return st.secrets["MISTRAL_API_KEY"]
    except:
        pass
    
    return None

MISTRAL_API_KEY = get_mistral_api_key()
client = Mistral(api_key=MISTRAL_API_KEY)

async def scrape_linkedin_content(url: str) -> str:
    """
    Attempts to scrape content from a LinkedIn URL.
    Since LinkedIn has strict anti-scraping, this is a best-effort approach.
    In a real-world scenario, a dedicated scraping API or browser automation would be better.
    """
    if not url or "linkedin.com" not in url:
        return ""
    
    try:
        async with httpx.AsyncClient(follow_redirects=True) as httpx_client:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = await httpx_client.get(url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Try to get meta description or specific tags
                meta_desc = soup.find("meta", property="og:description")
                if meta_desc:
                    return meta_desc.get("content", "")
                return soup.get_text(separator=' ', strip=True)[:1000] # Limit content
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    
    return ""

async def generate_comment(post_caption: str, post_link: str, profile_link: str, tone: str, model: str = "mistral-large-latest") -> str:
    # 1. Gather context
    post_context = ""
    if post_link:
        post_context = await scrape_linkedin_content(post_link)
    
    profile_context = ""
    if profile_link:
        profile_context = await scrape_linkedin_content(profile_link)
    
    # 2. Construct prompt
    system_prompt = (
        "You are an expert LinkedIn strategist and ghostwriter. Your goal is to generate a high-quality, "
        "natural-sounding LinkedIn comment based on a post and optional user profile context."
    )
    
    user_context_info = ""
    if profile_context:
        user_context_info = f"\nUser's Profile/Communication Style Context: {profile_context}"
    
    full_post_content = f"Post Caption: {post_caption}"
    if post_context:
        full_post_content += f"\nAdditional Post Context (from link): {post_context}"
    
    prompt = f"""
Analyze the following LinkedIn post:
{full_post_content}
{user_context_info}

Selected Tone: {tone}

Instructions:
- Generate a LinkedIn comment that is supportive and encouraging.
- The comment should reflect that the user learned something valuable from the post.
- Match the selected tone: {tone}.
- Align with the user's communication style if profile context is available.
- Keep the comment concise, natural, and avoid generic or exaggerated claims.
- Do NOT invent details if context is missing.
- Return ONLY the comment text.

Comment:
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    # 3. Call Mistral API
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=250
        )
        return chat_response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating comment: {str(e)}"

async def generate_caption(thoughts: str, profile_link: str, image_video_desc: str = "", model: str = "mistral-large-latest") -> str:
    # 1. Gather profile context
    profile_context = ""
    if profile_link:
        profile_context = await scrape_linkedin_content(profile_link)
    
    # 2. Construct prompt for personality analysis and caption generation
    system_prompt = (
        "You are an expert LinkedIn content creator. Your goal is to write highly engaging LinkedIn captions "
        "that follow a specific structure: Hook, Story, and Conclusion/CTA."
    )
    
    personality_info = ""
    if profile_context:
        personality_info = f"\nUser's Profile/Personality Context: {profile_context}"
    
    prompt = f"""
Write a LinkedIn caption based on the following:
User thoughts: {thoughts}
Media Description: {image_video_desc}
{personality_info}

Structure Requirements:
1. **Hook**: An intuitive or interesting first line to capture attention.
2. **Story**: A brief, engaging narrative based on the thoughts provided.
3. **Conclusion & CTA**: A summary and a clear call to action.

Guidelines:
- Align the tone and voice with the user's personality if profile context is available.
- If no profile context is available, use a professional yet approachable tone.
- Keep the caption natural, human, and conversational.
- Return ONLY the caption text.

Caption:
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    # 3. Call Mistral API
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=messages,
            temperature=0.8, # Slightly higher for creativity in captions
            max_tokens=600  # Captions are longer than comments
        )
        return chat_response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating caption: {str(e)}"

async def analyze_media(file_path: str = None, media_url: str = None) -> str:
    """Analyze an image or video using Mistral's vision capabilities."""
    image_data_url = None

    try:
        if file_path:
            # Handle local file
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                # Assuming image for now, as Pixtral handles images best
                # Support common image formats
                ext = os.path.splitext(file_path)[1].lower().replace(".", "")
                if ext not in ["jpg", "jpeg", "png", "webp"]:
                    ext = "jpeg"
                image_data_url = f"data:image/{ext};base64,{encoded_string}"
        
        elif media_url:
            # Handle URL
            # Note: For real-world use, we might want to download the image first
            # to ensure it's in a format Pixtral likes or to handle complex URLs (Drive, etc.)
            image_data_url = media_url

        if not image_data_url:
            return "No media provided for analysis."

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image or video in detail, focusing on elements relevant for a professional LinkedIn post. If it's a video, describe the main themes or visual narrative."},
                    {"type": "image_url", "image_url": image_data_url}
                ]
            }
        ]

        response = client.chat.complete(
            model="pixtral-12b-2409",
            messages=messages,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Media analysis failed: {str(e)}"
