# AI Color Palette Moodboard - Mobile Version

A beautiful, mobile-responsive web application for generating and exploring AI color palettes based on emotions.

## Features

✨ **Three Main Sections:**
1. **All Palettes** - Browse all 31 emotion-based color palettes
2. **Select Emotion** - Browse and explore individual emotions
3. **Upload Image** - Extract colors from images and match to emotions

🎨 **Core Features:**
- View all emotion palettes in a grid layout
- Extract dominant colors from uploaded images
- AI-powered emotion matching (based on color similarity)
- Download palettes in multiple formats (JSON, CSV, CSS, TXT)
- Fully responsive mobile design
- Dark mode support
- Touch-optimized interface

## Installation

### Requirements
- Python 3.8+
- Flask
- OpenCV (cv2)
- numpy
- scikit-learn
- Pillow

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements-mobile.txt
```

2. **Run the app:**
```bash
python app_mobile.py
```

3. **Open in browser:**
Navigate to `http://localhost:5000` on your device

## Mobile Access

### On the Same Network (Recommended)
Find your computer's IP address:
- **Windows:** `ipconfig` (Look for IPv4 Address)
- **Mac/Linux:** `ifconfig` (Look for inet address)

Then access: `http://<YOUR_IP>:5000` from your phone

### Localhost Testing
On the same machine: `http://localhost:5000`

## File Structure

```
├── app_mobile.py              # Flask application
├── emotion_data.py            # Emotion color palettes
├── image_palette.py           # Image processing functions
├── requirements-mobile.txt    # Python dependencies
├── templates/
│   └── index.html            # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css         # Mobile-responsive styles
│   └── js/
│       └── app.js            # JavaScript functionality
```

## Mobile Optimizations

✅ **Touch-Friendly**
- Large tap targets
- Swipe-friendly navigation
- Mobile-first design

✅ **Performance**
- Minimal dependencies
- Optimized assets
- Fast loading

✅ **Responsive**
- Works on all screen sizes
- Adaptive grid layouts
- Flexible spacing

✅ **Accessibility**
- High contrast colors
- Clear typography
- Proper touch targets

## API Endpoints

### GET /api/emotions
Get all emotions and their color palettes

### GET /api/emotion/<emotion_name>
Get a specific emotion's palette

### POST /api/extract-palette
Extract colors from uploaded image
- Body: multipart/form-data with 'file' field
- Returns: extracted colors, matched emotion, match score

### POST /api/export
Export palette data
- Body: JSON with colors, format, emotion
- Returns: formatted content and filename

## Emotion Palettes

The app includes 31 pre-defined emotion palettes:
- calm, luxury, trust, energy, nature
- joy, sadness, passion, serenity, mystery
- warmth, coolness, creativity, peace, elegance
- melancholy, adventurous, romantic, nostalgic, vibrant
- minimalist, dramatic, playful, sophisticated, fearless
- hopeful, zen, powerful, gentle, dark, bright

## Color Extraction Algorithm

The app uses:
1. **K-Means clustering** to find dominant colors
2. **Cosine similarity** to match against emotion palettes
3. **Normalization** to produce a 0-1 confidence score

## Browser Support

- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (iOS 12+)
- ✅ Edge (latest)

## Development

### Local Development
```bash
python app_mobile.py
# App runs on http://localhost:5000 with debug mode enabled
```

### Deployment

For production, use a proper WSGI server:
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_mobile:app
```

## Tips for Mobile Use

1. **Save to Home Screen:**
   - iOS: Tap Share → Add to Home Screen
   - Android: Chrome Menu → Install app

2. **Full Screen:**
   - Swipe between tabs smoothly
   - Tap colors to copy hex codes (future feature)

3. **Offline Support:**
   - Palettes are cached in browser after first load
   - Image upload requires internet connection

## Troubleshooting

**Can't access from phone on same network?**
- Check firewall settings
- Ensure both devices are on same Wi-Fi
- Try using IP address instead of hostname

**Image upload fails?**
- Check file size (max 16MB)
- Use PNG or JPG format
- Ensure sufficient server disk space

**Slow performance?**
- Check connection speed
- Try uploading smaller images
- Clear browser cache

## License

This project is open source and available under the MIT License.

## Version Notes

**Mobile (Flask) vs Desktop (Streamlit):**
- **Mobile Version** (`app_mobile.py`): Optimized for phones/tablets
- **Desktop Version** (`app.py`): Full-featured Streamlit app

Run both versions simultaneously on different ports!

---

**Enjoy creating beautiful color palettes! 🎨**
