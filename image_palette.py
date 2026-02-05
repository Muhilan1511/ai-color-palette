import streamlit as st
from PIL import Image
import numpy as np
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity

def extract_colors_from_image(image_path, num_colors=5):
    """Extract dominant colors from an image."""
    try:
        img = Image.open(image_path)
        img = img.resize((100, 100))
        img = img.convert('RGB')
        pixels = np.array(img).reshape(-1, 3)
        colors = ['#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b)) for r,g,b in pixels]
        color_counts = Counter(colors)
        dominant_colors = [color for color, _ in color_counts.most_common(num_colors)]
        return dominant_colors
    except Exception as e:
        st.error(f"Error extracting colors: {e}")
        return []

def match_emotion_to_palette(colors, emotion_colors):
    """Match extracted colors to nearest emotion palette.
       Uses mean RGB per-palette + cosine similarity and returns a normalized score in [0,1]."""
    def hex_to_rgb(hex_color):
        h = hex_color.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    # compute mean RGB of extracted colors
    extracted_rgb = np.array([hex_to_rgb(c) for c in colors], dtype=float)
    if extracted_rgb.size == 0:
        return None, 0.0
    extracted_mean = extracted_rgb.mean(axis=0).reshape(1, -1)

    best_match = None
    best_score = -1.0

    for emotion, palette in emotion_colors.items():
        palette_rgb = np.array([hex_to_rgb(c) for c in palette], dtype=float)
        if palette_rgb.size == 0:
            continue
        palette_mean = palette_rgb.mean(axis=0).reshape(1, -1)

        sim = cosine_similarity(extracted_mean, palette_mean)[0, 0]  # in [-1, 1]
        sim_norm = (sim + 1.0) / 2.0  # map to [0,1]

        if sim_norm > best_score:
            best_score = sim_norm
            best_match = emotion

    return best_match, float(best_score)
