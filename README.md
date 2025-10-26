🧠 AI-Powered Image Editing Platform

🚀 A Next-Generation Generative AI Web App for Intuitive Image Editing

This project is a full-stack AI-powered web application that enables users to upload, edit, search, and manage images using natural language commands.
Unlike traditional editors like Photoshop, this platform uses Generative AI (OpenAI GPT & Embedding APIs) to perform image editing, caption generation, and semantic search — all through simple text instructions.
🪄 Overview

The AI-Powered Image Editing Platform allows users to:
	•	Upload and manage multiple images
	•	Generate AI-based captions and embeddings
	•	Perform image edits using natural language prompts (e.g., “remove the background”, “add a sunset sky”)
	•	Track version history for each edited image
	•	Search across the image library using natural language queries (e.g., “show images with trees”)

This project is designed as a portfolio-ready MVP demonstrating full-stack AI integration using Streamlit, OpenAI APIs, and Python.
AI-Powered Image Editing Platform/
├── app.py                 # Main Streamlit App
├── prompt_handler.py      # Edit Prompt Testing Script
├── data/
│   ├── images/            # Uploaded + Edited Images
│   └── metadata.json      # Metadata with captions, embeddings & versions
├── requirements.txt       # Dependencies
├── .env                   # API Key (Excluded via .gitignore)
├── .gitignore
└── README.md              # Project Documentation

⚙️ Setup Instructions
git clone https://github.com/siddharth1956/ai-image-editing-platform.git
cd ai-image-editing-platform

2️⃣ Create your environment
python3 -m venv venv
source venv/bin/activate

4️⃣ Add your OpenAI API Key

Create a .env file in the project root:
OPENAI_API_KEY=your_openai_key_here

5️⃣ Run the app
streamlit run app.py

🧑‍💻 Usage Guide

🔹 Upload Images
	•	Click Upload in the sidebar to add one or more images (.png, .jpg, .jpeg).
	•	The app automatically generates basic captions and embeddings.

🔹 Search with Natural Language
	•	In the sidebar search box, type queries like:
	•	sunset
	•	mountain
	•	person wearing red
	•	The app uses semantic similarity to find matching images.

🔹 Edit an Image
	•	Click View / Edit on any image.
	•	Enter a natural prompt like:
	add a blue sky
remove the person on the left
make background white
