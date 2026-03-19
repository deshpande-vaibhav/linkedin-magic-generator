// Configuration: Set this to your live backend URL when deployed
// If running locally, it defaults to localhost:8000
const API_BASE_URL = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' 
    ? 'http://127.0.0.1:8000' 
    : 'https://your-backend-app.onrender.com'; // User will need to update this

// Tab Switching Logic
document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', () => {
        // Update tabs
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        // Update sections
        const target = button.getAttribute('data-target');
        document.querySelectorAll('.generator-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(target).classList.add('active');

        // Reset output
        document.getElementById('output-section').style.display = 'none';
    });
});

// Common UI Elements
const loader = document.getElementById('loader');
const outputSection = document.getElementById('output-section');
const generatedOutput = document.getElementById('generated-output');
const outputTitle = document.getElementById('output-title');

// Upload Box Logic
const uploadBox = document.getElementById('upload-box');
const mediaFileInput = document.getElementById('media_file');
const fileNameDisplay = document.getElementById('file-name');

uploadBox.addEventListener('click', () => mediaFileInput.click());

mediaFileInput.addEventListener('change', () => {
    if (mediaFileInput.files.length > 0) {
        fileNameDisplay.textContent = `Selected: ${mediaFileInput.files[0].name}`;
    } else {
        fileNameDisplay.textContent = '';
    }
});

// Magic Comment Generation
document.getElementById('generate-comment-btn').addEventListener('click', async () => {
    const postCaption = document.getElementById('post_caption').value;
    const postLink = document.getElementById('post_link').value;
    const profileLink = document.getElementById('profile_link_comment').value;
    const tone = document.getElementById('tone').value;
    const model = document.getElementById('model_comment').value;

    if (!postCaption) {
        alert('Please enter a post caption');
        return;
    }

    await generateContent(`${API_BASE_URL}/generate`, {
        post_caption: postCaption,
        post_link: postLink,
        profile_link: profileLink,
        tone: tone,
        model: model
    }, 'Magic Comment Generated');
});

// Magic Caption Generation
document.getElementById('generate-caption-btn').addEventListener('click', async () => {
    const thoughts = document.getElementById('user_thoughts').value;
    const mediaUrl = document.getElementById('media_url').value;
    const mediaFile = document.getElementById('media_file').files[0];
    const profileLink = document.getElementById('profile_link_caption').value;
    const model = document.getElementById('model_caption').value;

    if (!thoughts) {
        alert('Please enter your thoughts or a topic');
        return;
    }

    const formData = new FormData();
    formData.append('thoughts', thoughts);
    formData.append('profile_link', profileLink);
    formData.append('media_url', mediaUrl);
    formData.append('model', model);
    if (mediaFile) {
        formData.append('media_file', mediaFile);
    }

    await generateContent(`${API_BASE_URL}/generate_caption`, formData, 'Magic Caption Generated');
});

// Unified Generation Helper
async function generateContent(url, body, title) {
    const activeBtn = document.querySelector('.generator-section.active .generate-btn');
    activeBtn.disabled = true;
    loader.style.display = 'block';
    outputSection.style.display = 'none';

    try {
        const isFormData = body instanceof FormData;
        const response = await fetch(url, {
            method: 'POST',
            headers: isFormData ? {} : { 'Content-Type': 'application/json' },
            body: isFormData ? body : JSON.stringify(body),
        });

        if (!response.ok) {
            throw new Error('Failed to generate content');
        }

        const data = await response.json();
        generatedOutput.textContent = data.comment || data.caption;
        outputTitle.textContent = title;
        outputSection.style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong. Please check if the backend is running and try again.');
    } finally {
        activeBtn.disabled = false;
        loader.style.display = 'none';
    }
}

// Copy to Clipboard
document.getElementById('copy-btn').addEventListener('click', () => {
    const text = generatedOutput.textContent;
    navigator.clipboard.writeText(text).then(() => {
        const copyBtn = document.getElementById('copy-btn');
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);
    });
});
