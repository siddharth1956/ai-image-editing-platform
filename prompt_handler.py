# prompt_handler.py
"""
Standalone prompt handler to test prompt formatting and OpenAI image edits
(uses openai>=1.0.0 client interface).
Saves edited image as prompt_handler_output.png.
"""

import os
import io
import base64
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from openai import OpenAI

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise SystemExit("Set OPENAI_API_KEY in .env before running this script.")

client = OpenAI(api_key=OPENAI_KEY)

def format_edit_prompt(user_prompt: str, style: str = None) -> str:
    template = ("Apply the following edit to the image: {0}. "
                "Keep faces natural and avoid adding logos or text. "
                "Return a natural-looking edit that preserves resolution.")
    p = template.format(user_prompt)
    if style:
        p = p + " Style: {0}.".format(style)
    return p

def test_edit(image_path: str, user_prompt: str, out_path: str = "prompt_handler_output.png"):
    img_p = Path(image_path)
    if not img_p.exists():
        raise FileNotFoundError("Image not found: {0}".format(image_path))

    im = Image.open(img_p).convert("RGBA")
    im.thumbnail((1024, 1024))
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0)

    prompt = format_edit_prompt(user_prompt, style="photorealistic")

    # call client.images.edit (new OpenAI client)
    try:
        with open(img_p, "rb") as f_image:
            response = client.images.edit(
                model="gpt-image-1",
                image=[f_image],
                prompt=prompt,
                size="1024x1024",
                n=1
            )
        # extract base64
        b64 = None
        try:
            b64 = response.data[0].b64_json
        except Exception:
            b64 = response.get("data", [{}])[0].get("b64_json")

        if not b64:
            raise RuntimeError("No image data returned by API. Response summary: {0}".format(str(type(response))))

        edited_bytes = base64.b64decode(b64)
        Path(out_path).write_bytes(edited_bytes)
        print("Saved edited image to {0}".format(out_path))
    except Exception as e:
        print("API edit failed: {0}".format(e))
        # For debugging you can print(response) here (do not share keys).
        raise

if __name__ == "__main__":
    # EDIT THESE: provide a real image in data/images/
    sample_image = "data/images/<replace_with_existing_image_filename>.png"
    user_prompt = "remove the background and add a bright blue sky"
    test_edit(sample_image, user_prompt)