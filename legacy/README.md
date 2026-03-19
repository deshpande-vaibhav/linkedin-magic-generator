# 🪄 LinkedIn Comment Magic - AI-Powered Engagement

LinkedIn Comment Magic is a premium, AI-powered tool designed to generate high-quality, contextually relevant LinkedIn comments and captions. Leveraging Mistral AI's powerful models, it helps users boost their engagement with style and ease.

## ✨ Key Features

- **Magic Comment Generator**: Generate thoughtful, funny, or professional comments based on post captions and links.
- **Magic Caption Generator**: Create viral-ready captions from your thoughts, including advanced **Media Analysis** for images and videos.
- **Multi-Model Support**: Use **Mistral Large** for high-quality reasoning or **Mistral Small** for speed. Includes **Pixtral** for vision tasks.
- **Premium UI**: A modern, sleek Glassmorphism design built with Streamlit.
- **Context Awareness**: Optional LinkedIn profile and post link integration for highly personalized responses.

## 🚀 Quick Start (Local)

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/deshpande-vaibhav/linkedin-magic-generator.git
   cd linkedin-magic-generator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Key**:
   Create a `.env` file in the root directory:
   ```env
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

4. **Run the App**:
   ```bash
   streamlit run streamlit_app.py
   ```

## 🌐 Deployment (Streamlit Cloud)

1. Push this repository to your GitHub account.
2. Sign in to [Streamlit Cloud](https://share.streamlit.io/).
3. Connect this repository and set `streamlit_app.py` as the main file.
4. Add your `MISTRAL_API_KEY` in the **Advanced Settings > Secrets** section of Streamlit Cloud.

## 🔒 Security

This project uses `.gitignore` to ensure your `.env` file and sensitive credentials are never published. Always use Environment Variables or Streamlit Secrets for API keys.

## 🛠️ Built With

- **Mistral AI** (Large, Small, Pixtral)
- **Streamlit** (Frontend & Deployment)
- **FastAPI** (Optional Backend Logic)
- **BeautifulSoup4** (Content Scraping)

---
© 2026 LinkedIn Comment Magic. Optimized for professional engagement.
