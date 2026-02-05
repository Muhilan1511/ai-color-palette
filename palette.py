from emotion_data import emotion_colors

def generate_palette(emotion):
    """Generate a color palette based on emotion."""
    if emotion in emotion_colors:
        return emotion_colors[emotion]
    return []