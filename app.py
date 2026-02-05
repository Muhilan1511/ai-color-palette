import streamlit as st
import numpy as np
import cv2
import json
import time
from emotion_data import emotion_colors
from image_palette import extract_colors_from_image, match_emotion_to_palette

st.set_page_config(
    page_title="AI Color Palette Generator",
    layout="centered"
)

# Add CSS animations (ONLY ONCE, near top)
st.markdown(
    """
    <style>
    .fade-in {
        animation: fadeIn 0.8s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎨 AI Color Palette Moodboard")

# Tab navigation
tab1, tab2, tab3 = st.tabs(["All Palettes", "Select Emotion", "Upload Image"])

# Tab 1: Display all emotion palettes
with tab1:
    st.subheader("All Emotion Color Palettes")
    
    cols = st.columns(3)
    col_index = 0
    
    for emotion, colors in emotion_colors.items():
        with cols[col_index % 3]:
            st.write(f"**{emotion.title()}**")
            color_cols = st.columns(len(colors))
            for i, color in enumerate(colors):
                with color_cols[i]:
                    st.markdown(
                        f'<div style="background-color: {color}; width: 100%; height: 80px; border-radius: 8px;"></div>',
                        unsafe_allow_html=True
                    )
                    st.caption(color)
        col_index += 1
    
    # Export all palettes
    export_col1, export_col2, export_col3 = st.columns(3)
    with export_col1:
        if st.button("📥 JSON"):
            json_data = json.dumps(emotion_colors, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="all_palettes.json",
                mime="application/json"
            )
    with export_col2:
        if st.button("📄 TXT"):
            txt_data = "AI COLOR PALETTE MOODBOARD\n" + "="*50 + "\n\n"
            for emotion, colors in emotion_colors.items():
                txt_data += f"{emotion.upper()}\n"
                for color in colors:
                    txt_data += f"  {color}\n"
                txt_data += "\n"
            st.download_button(
                label="Download TXT",
                data=txt_data,
                file_name="all_palettes.txt",
                mime="text/plain"
            )
    with export_col3:
        if st.button("📋 CSV"):
            csv_data = "Emotion,Color1,Color2,Color3\n"
            for emotion, colors in emotion_colors.items():
                csv_data += f"{emotion}," + ",".join(colors) + "\n"
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="all_palettes.csv",
                mime="text/csv"
            )

# Tab 2: Interactive selector
with tab2:
    st.subheader("Select an Emotion")
    
    emotion = st.selectbox("Choose:", list(emotion_colors.keys()))
    
    if emotion:
        colors = emotion_colors[emotion]
        st.subheader(f"Colors for '{emotion.title()}'")
        
        cols = st.columns(len(colors))
        for i, color in enumerate(colors):
            with cols[i]:
                st.markdown(
                    f'<div style="background-color: {color}; width: 100%; height: 120px; border-radius: 8px; border: 2px solid #ccc;"></div>',
                    unsafe_allow_html=True
                )
                st.write(color)
        
        # Export single palette
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("JSON"):
                json_data = json.dumps({emotion: colors}, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"{emotion}_palette.json",
                    mime="application/json"
                )
        with col2:
            if st.button("TXT"):
                txt_data = f"{emotion.upper()} PALETTE\n" + "="*30 + "\n\n"
                for i, color in enumerate(colors, 1):
                    txt_data += f"Color {i}: {color}\n"
                st.download_button(
                    label="Download TXT",
                    data=txt_data,
                    file_name=f"{emotion}_palette.txt",
                    mime="text/plain"
                )
        with col3:
            if st.button("CSS"):
                css_data = f":root {{\n"
                for i, color in enumerate(colors):
                    css_data += f"  --color-{i+1}: {color};\n"
                css_data += "}"
                st.download_button(
                    label="Download CSS",
                    data=css_data,
                    file_name=f"{emotion}_palette.css",
                    mime="text/css"
                )

# Tab 3: Upload image
with tab3:
    st.subheader("📷 Upload Image to Detect Color Palette")
    
    uploaded_file = st.file_uploader(
        "Upload an image (PNG/JPG)",
        type=["png", "jpg", "jpeg"]
    )
    
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        st.image(image_rgb, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Extract Color Palette"):
            temp_path = "temp_image.jpg"
            cv2.imwrite(temp_path, image)
            
            with st.spinner("🎨 Analyzing image and extracting color palette..."):
                palette = extract_colors_from_image(temp_path, num_colors=5)
                matched_emotion, score = match_emotion_to_palette(palette, emotion_colors)
            
            st.subheader("🎨 Animated Color Palette")
            
            for color in palette:
                st.markdown(
                    f"""
                    <div class="fade-in" style="
                        background-color:{color};
                        padding:18px;
                        border-radius:12px;
                        margin-bottom:12px;
                        color:white;
                        font-weight:bold;
                        text-align:center;
                        ">
                        {color}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                time.sleep(0.2)
            
            if matched_emotion:
                matched_palette = emotion_colors.get(matched_emotion, [])
                st.subheader(f"📊 Best Match: {matched_emotion.title()} ({score*100:.2f}%)")
                mp_cols = st.columns(len(matched_palette))
                for i, color in enumerate(matched_palette):
                    with mp_cols[i]:
                        st.markdown(
                            f'<div style="background-color: {color}; width: 100%; height: 80px; border-radius: 6px; border:1px solid #222;"></div>',
                            unsafe_allow_html=True
                        )
                        st.caption(color)
                
                # Export extracted palette
                export_col1, export_col2, export_col3 = st.columns(3)
                with export_col1:
                    if st.button("JSON Extract"):
                        json_data = json.dumps({"extracted": palette, "emotion": matched_emotion}, indent=2)
                        st.download_button(
                            label="Download JSON",
                            data=json_data,
                            file_name="extracted_palette.json",
                            mime="application/json"
                        )
                with export_col2:
                    if st.button("TXT Extract"):
                        txt_data = f"EXTRACTED PALETTE\n" + "="*30 + "\n"
                        txt_data += f"Matched Emotion: {matched_emotion.upper()}\n"
                        txt_data += f"Match Score: {score*100:.2f}%\n\n"
                        for i, color in enumerate(palette, 1):
                            txt_data += f"Color {i}: {color}\n"
                        st.download_button(
                            label="Download TXT",
                            data=txt_data,
                            file_name="extracted_palette.txt",
                            mime="text/plain"
                        )
                with export_col3:
                    if st.button("CSS Extract"):
                        css_data = f":root {{\n"
                        for i, color in enumerate(palette):
                            css_data += f"  --color-{i+1}: {color};\n"
                        css_data += "}"
                        st.download_button(
                            label="Download CSS",
                            data=css_data,
                            file_name="extracted_palette.css",
                            mime="text/css"
                        )