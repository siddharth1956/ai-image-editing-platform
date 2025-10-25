# app.py — Week 3 (Image Search + Backend Enhancements)

import os
import io
import json
import uuid
import base64
import shutil
import numpy as np
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
import streamlit as st

# Load environment variables
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Import OpenAI client
from openai import OpenAI
client = OpenAI(api_key=OPENAI_KEY)

# Directories
DATA_DIR = Path("data")
IMAGES_DIR = DATA_DIR / "images"
METADATA_PATH = DATA_DIR / "metadata.json"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
if not METADATA_PATH.exists():
    with open(METADATA_PATH, "w") as f:
        json.dump({"images": []}, f, indent=2)

# ---------- UTILITY FUNCTIONS ----------
def load_metadata():
    with open(METADATA_PATH, "r") as f:
        return json.load(f)

def save_metadata(meta):
    with open(METADATA_PATH, "w") as f:
        json.dump(meta, f, indent=2, sort_keys=True, default=str)

def get_embedding(text: str):
    """Generate an embedding for text using OpenAI embedding API."""
    if not text or text.strip() == "":
        return None
    try:
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return emb.data[0].embedding
    except Exception as e:
        st.error(f"Embedding generation failed: {e}")
        return None

def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ---------- BACKEND LOGIC ----------
def add_image_record(filename, orig_name, caption):
    meta = load_metadata()
    emb = get_embedding(caption)
    record = {
        "id": str(uuid.uuid4()),
        "filename": filename,
        "orig_name": orig_name,
        "uploaded_at": datetime.utcnow().isoformat() + "Z",
        "caption": caption,
        "embedding": emb,
        "versions": [
            {
                "version_id": 1,
                "filename": filename,
                "note": "original upload",
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
        ]
    }
    meta["images"].append(record)
    save_metadata(meta)
    return record

def add_new_version(image_id, new_filename, note):
    meta = load_metadata()
    for img in meta["images"]:
        if img["id"] == image_id:
            new_ver = {
                "version_id": len(img["versions"]) + 1,
                "filename": new_filename,
                "note": note,
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
            img["versions"].append(new_ver)
            save_metadata(meta)
            return new_ver
    return None

def find_by_id(image_id):
    meta = load_metadata()
    for img in meta["images"]:
        if img["id"] == image_id:
            return img
    return None

def update_image_caption(image_id, new_caption):
    meta = load_metadata()
    for img in meta["images"]:
        if img["id"] == image_id:
            img["caption"] = new_caption
            img["embedding"] = get_embedding(new_caption)
            save_metadata(meta)
            return img
    return None

# ---------- IMAGE EDITING ----------
def apply_edit_api(image_path: Path, prompt: str):
    """Edit image using GPT-image-1."""
    try:
        with open(image_path, "rb") as f_image:
            response = client.images.edit(
                model="gpt-image-1",
                image=[f_image],
                prompt=prompt,
                size="1024x1024",
                n=1
            )
        b64 = response.data[0].b64_json
        edited_bytes = base64.b64decode(b64)
        new_name = "edit_" + image_path.name
        out_path = IMAGES_DIR / new_name
        with open(out_path, "wb") as out:
            out.write(edited_bytes)
        return new_name
    except Exception as e:
        st.warning(f"OpenAI edit failed ({e}); simulated copy created.")
        edited_name = "edit_" + image_path.name
        shutil.copy(image_path, IMAGES_DIR / edited_name)
        return edited_name

# ---------- STREAMLIT APP ----------
st.set_page_config(page_title="AI Image Editor — Week 3", layout="wide")
st.title("🧠 AI-Powered Image Editing Platform — Week 3: Search + Backend")

# Sidebar
with st.sidebar:
    st.header("Upload")
    uploaded_files = st.file_uploader(
        "Upload images",
        type=["png", "jpg", "jpeg", "webp", "bmp"],
        accept_multiple_files=True
    )
    st.markdown("---")
    st.header("Search")
    query = st.text_input("Search (e.g., 'sunset', 'mountain', 'sky')")
    st.markdown("---")
    st.caption("Metadata in data/metadata.json")

# Upload logic
if uploaded_files:
    for uploaded in uploaded_files:
        uid = str(uuid.uuid4())
        ext = os.path.splitext(uploaded.name)[1].lower()
        target_name = uid + ext
        target_path = IMAGES_DIR / target_name
        with open(target_path, "wb") as out:
            out.write(uploaded.getvalue())
        # Basic caption + embedding
        with Image.open(target_path) as im:
            w, h = im.size
        caption = f"Image {target_name} with size {w}x{h}"
        rec = add_image_record(target_name, uploaded.name, caption)
        st.sidebar.success(f"Saved: {uploaded.name}")

# Load metadata
meta = load_metadata()
images = meta.get("images", [])

# ---------- SEARCH LOGIC ----------
if query.strip():
    query_emb = get_embedding(query)
    scored = []
    for img in images:
        if img.get("embedding"):
            score = cosine_similarity(query_emb, img["embedding"])
            scored.append((score, img))
    scored.sort(reverse=True, key=lambda x: x[0])
    filtered = [img for _, img in scored[:8]]
else:
    filtered = images

# ---------- IMAGE LIBRARY ----------
st.markdown("## 🖼️ Image Library")
cols_per_row = 4
rows = (len(filtered) + cols_per_row - 1) // cols_per_row

for row in range(rows):
    cols = st.columns(cols_per_row)
    start = row * cols_per_row
    for i, col in enumerate(cols):
        idx = start + i
        if idx >= len(filtered):
            break
        rec = filtered[idx]
        img_path = IMAGES_DIR / rec["filename"]
        try:
            col.image(str(img_path), use_column_width=True)
        except:
            continue
        col.caption(f"{rec['orig_name']} | {rec['caption']}")
        if col.button(f"View/Edit {rec['id'][-4:]}", key=rec["id"]):
            st.session_state["selected_image"] = rec["id"]

st.markdown("---")

# ---------- IMAGE DETAIL ----------
selected_id = st.session_state.get("selected_image", None)
if selected_id:
    rec = find_by_id(selected_id)
    if rec:
        st.markdown("## 🖼️ Image Detail")
        st.image(str(IMAGES_DIR / rec["filename"]), width=600)
        st.write(f"**Caption:** {rec['caption']}")
        st.write(f"**Uploaded at:** {rec['uploaded_at']}")

        st.markdown("### ✏️ AI Image Editing")
        prompt = st.text_input("Enter edit prompt", key="edit_prompt")
        if st.button("Apply Edit"):
            new_file = apply_edit_api(IMAGES_DIR / rec["filename"], prompt)
            add_new_version(selected_id, new_file, prompt)
            st.success("Edit complete. Version saved.")

        st.markdown("### 🕓 Version History")
        for v in rec["versions"]:
            v_path = IMAGES_DIR / v["filename"]
            if v_path.exists():
                st.image(str(v_path), width=250, caption=f"v{v['version_id']}: {v['note']}")