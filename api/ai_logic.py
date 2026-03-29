import os
import httpx
import base64
from bs4 import BeautifulSoup
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv(override=True)

def get_mistral_client():
    key = os.getenv("MISTRAL_API_KEY")
    if not key:
        # Try Streamlit secrets as fallback
        try:
            import streamlit as st
            if "MISTRAL_API_KEY" in st.secrets:
                key = st.secrets["MISTRAL_API_KEY"]
        except:
            pass
    
    if not key:
        return None
    
    key = key.strip()
    return Mistral(api_key=key)

async def scrape_linkedin_content(url: str) -> str:
    """Best-effort LinkedIn scraping."""
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
                meta_desc = soup.find("meta", property="og:description")
                if meta_desc:
                    return meta_desc.get("content", "")
                return soup.get_text(separator=' ', strip=True)[:1000]
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    
    return ""

async def generate_comment(post_caption: str, post_link: str, profile_link: str, tone: str, model: str = "mistral-large-latest") -> str:
    client = get_mistral_client()
    if not client:
        return "Error: MISTRAL_API_KEY not found in environment variables."

    post_context = ""
    if post_link:
        post_context = await scrape_linkedin_content(post_link)
    
    profile_context = ""
    if profile_link:
        profile_context = await scrape_linkedin_content(profile_link)
    
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
    
    try:
        chat_response = await client.chat.complete_async(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=250
        )
        return chat_response.choices[0].message.content.strip()
    except Exception as e:
        if "401" in str(e):
            return "Error: Invalid Mistral API Key. Please check your .env file."
        return f"Error generating comment: {str(e)}"

async def generate_caption(thoughts: str, profile_link: str, image_video_desc: str = "", model: str = "mistral-large-latest") -> str:
    client = get_mistral_client()
    if not client:
        return "Error: MISTRAL_API_KEY not found in environment variables."

    profile_context = ""
    if profile_link:
        profile_context = await scrape_linkedin_content(profile_link)
    
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
    
    try:
        chat_response = await client.chat.complete_async(
            model=model,
            messages=messages,
            temperature=0.8,
            max_tokens=600
        )
        return chat_response.choices[0].message.content.strip()
    except Exception as e:
        if "401" in str(e):
            return "Error: Invalid Mistral API Key. Please check your .env file."
        return f"Error generating caption: {str(e)}"

async def analyze_media(file_path: str = None, media_url: str = None) -> str:
    """Analyze an image or video using Mistral's vision capabilities."""
    client = get_mistral_client()
    if not client:
        return "Error: MISTRAL_API_KEY not found."

    image_data_url = None

    try:
        if file_path:
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                ext = os.path.splitext(file_path)[1].lower().replace(".", "")
                if ext not in ["jpg", "jpeg", "png", "webp"]:
                    ext = "jpeg"
                image_data_url = f"data:image/{ext};base64,{encoded_string}"
        
        elif media_url:
            image_data_url = media_url

        if not image_data_url:
            return "No media provided for analysis."

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image or video in detail, focusing on elements relevant for a professional LinkedIn post."},
                    {"type": "image_url", "image_url": image_data_url}
                ]
            }
        ]

        response = await client.chat.complete_async(
            model="pixtral-12b-2409",
            messages=messages,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        if "401" in str(e):
            return "Error: Invalid Mistral API Key."
        return f"Media analysis failed: {str(e)}"
