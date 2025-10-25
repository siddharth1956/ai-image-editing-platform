This is your short project summary and architecture write-up (required for Week 1 submission).
Create a new Markdown file called README.md and paste the following template:
# AI-Powered Image Editing Platform — Week 1

## 🎯 Objective
Build the foundation of an AI-first image editing platform that allows users to upload, view, and manage images with automatic captioning and search.

## 🧩 Features (Week 1)
- Upload one or multiple images
- Store image metadata locally (`data/metadata.json`)
- Auto-generate captions (local fallback; Vision API ready)
- Display all images in a grid view
- Natural-language search (substring)
- Image detail page + version history structure

## 🛠️ Tech Stack
- **Frontend:** Streamlit  
- **Backend:** Local JSON (no external DB yet)  
- **Language:** Python 3.9+  
- **Libraries:** Streamlit, Pillow  

## 📁 Project Structure
AI-Powered Image Editing Platform/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
├── images/
└── metadata.json

## 🚀 How to Run
```bash
# Clone repo and enter folder
git clone <repo-link>
cd "AI-Powered Image Editing Platform"

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py

🧠 Architecture Summary
	1.	Upload Interface: Users upload images via Streamlit sidebar.
	2.	Storage: Images are saved in data/images/; metadata stored in data/metadata.json.
	3.	Captioning: A local placeholder generates captions (to be replaced by a Vision API).
	4.	Search: Simple substring match on captions and filenames.
	5.	Version Tracking: Each image has a versions array for future edited versions.
