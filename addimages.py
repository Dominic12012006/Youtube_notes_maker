import re
import os
import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests

def download_image(query, save_path):
    with DDGS() as ddgs:
        results = ddgs.images(query)
        for r in results:
            try:
                img_url = r['image']
                response = requests.get(img_url, timeout=10)
                if "image" not in response.headers["Content-Type"]:
                    continue  # Skip non-image content

                # Convert to PNG using Pillow
                image = Image.open(BytesIO(response.content)).convert("RGB")
                image.save(save_path, format="PNG")
                print(f"Downloaded and saved: {save_path}")
                return True
            except Exception as e:
                print("Image download failed:", e)
                continue
    return False

# def download_image(query, save_path):
#     with DDGS() as ddgs:
#         results = ddgs.images(query)
#         for r in results:
#             try:
#                 img_url = r['image']
#                 img_data = requests.get(img_url).content
#                 with open(save_path, 'wb') as f:
#                     f.write(img_data)
#                 print(f"Downloaded: {save_path}")
#                 return True
#             except Exception as e:
#                 print("Image download failed:", e)
#                 continue
#     return False

def insert_images(text, image_dir="images"):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    def replacer(match):
        query = match.group(1).strip()
        filename = "_".join(query.lower().split()) + ".png"
        filepath = os.path.join(image_dir, filename)

        if download_image(query, filepath):
            return f"![{query}]({filepath})"
        else:
            return f"**[Image not available for: {query}]**"

    return re.sub(r"\$\$\[(.+?)\]\$\$", replacer, text)

# ---- Example usage ----
# with open("summary.txt", "r", encoding="utf-8") as f:
#     summary = f.read()

# updated_summary = insert_images(summary)

# with open("sumfinal.md", "w", encoding="utf-8") as f:
#     f.write(updated_summary)

# print("Summary with images saved as sumfinal.md")
