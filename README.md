# 🪄 LinkedIn Magic Generator

A premium AI-powered tool to generate highly engaging LinkedIn comments and captions. Built with **Next.js 14**, **Tailwind CSS**, and **FastAPI**, optimized for **Vercel** deployment.

## ✨ Features

- **Magic Comment Generator**: Generate insightful, professional, or casual comments for any LinkedIn post.
- **Magic Caption Generator**: Create viral-ready captions from your thoughts and media (images/videos).
- **Premium UI**: Modern, glassmorphism design with LinkedIn brand aesthetics and smooth animations.
- **AI-Powered**: Leverages Mistral AI's latest models for intelligent content generation.

## 🚀 Tech Stack

- **Frontend**: Next.js (App Router), Tailwind CSS, Framer Motion, Lucide React.
- **Backend**: FastAPI (Python) serving as Vercel Serverless Functions.
- **Models**: Mistral Large & Mistral Small.

## 🛠️ Local Development

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/deshpande-vaibhav/linkedin-magic-generator.git
    cd linkedin-magic-generator
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Set up environment variables**:
    Create a `.env` file in the root and add your Mistral API key:
    ```env
    MISTRAL_API_KEY=your_api_key_here
    ```

4.  **Run the development server**:
    ```bash
    npm run dev
    ```

## 🌐 Deployment on Vercel

This project is structured for a unified deployment on Vercel:
- The `api/` directory contains the Python serverless functions.
- The root directory contains the Next.js application.

Simply connect your GitHub repository to Vercel and it will automatically detect and deploy both the frontend and backend.
