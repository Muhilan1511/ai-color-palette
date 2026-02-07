# 🚀 Quick Start - Mobile Version

## Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements-mobile.txt
```

### 2. Run the Mobile App
```bash
python app_mobile.py
```

### 3. Open on Your Phone
- **Same Computer:** `http://localhost:5000`
- **Phone on Same Network:** 
  1. Find your computer IP (Windows: `ipconfig`)
  2. Go to `http://<YOUR_IP>:5000` on phone

---

## What You Get

✅ **Three Tabs:**
- **All Palettes** - Grid view of 31 emotion-based color palettes
- **Select Emotion** - Pick and explore individual emotions
- **Upload Image** - Extract colors from photos + AI emotion matching

✅ **Export Options:**
- JSON, CSV, CSS, TXT formats

✅ **Mobile-Optimized:**
- Touch-friendly interface
- Works on any screen size
- Dark mode support

---

## Features

📱 **Mobile First Design**
- Sticky navigation
- Swipe-friendly tabs
- Touch-optimized buttons

🎨 **Image Analysis**
- Upload photo
- Extract 5 dominant colors
- AI matches to emotion
- Shows confidence score

📥 **Download Palettes**
- JSON for developers
- CSS for web design
- CSV for spreadsheets
- TXT for reference

---

## File Changes

**New Files Created:**
- `app_mobile.py` - Flask web app
- `templates/index.html` - Mobile interface
- `static/css/style.css` - Responsive styles
- `static/js/app.js` - App functionality
- `requirements-mobile.txt` - Dependencies
- `MOBILE_README.md` - Full documentation

**Existing Files (Unchanged):**
- `emotion_data.py` - Color palettes (reused)
- `image_palette.py` - Image processing (reused)

---

## Mobile Browser Tips

📲 **iOS:**
- Tap Share → "Add to Home Screen" for app-like experience

📱 **Android:**
- Long-press → "Install app" for app-like experience

💡 **Pro Tips:**
- Upload clear, colorful images for best results
- Max image size: 16MB
- Supports PNG and JPG formats

---

## Troubleshooting

❌ **"Cannot connect from phone"**
- Check both devices on same Wi-Fi
- Use IP address, not localhost
- Check Windows Firewall isn't blocking port 5000

❌ **"Image upload fails"**
- Use PNG or JPG format
- Check file is under 16MB
- Ensure good internet connection

❌ **"Colors don't look right"**
- Use clear, well-lit photos
- Try different images for comparison

---

## Run Both Versions

You can run both Streamlit and Flask versions simultaneously:

**Terminal 1 - Desktop Version:**
```bash
streamlit run app.py
```

**Terminal 2 - Mobile Version:**
```bash
python app_mobile.py
```

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Run `python app_mobile.py`
3. ✅ Visit `http://localhost:5000`
4. ✅ Try uploading an image!

**Enjoy! 🎨**
