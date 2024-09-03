import pytesseract
from src.utils.capture import capture_screen

def search_word_on_screen(phrase):
    screen_image = capture_screen()
    screen_image = screen_image.convert('L')
    screen_image = screen_image.point(lambda p: p > 128 and 255)

    d = pytesseract.image_to_data(screen_image, output_type=pytesseract.Output.DICT, config='--psm 6')
    words = d['text']
    left = d['left']
    top = d['top']
    width = d['width']
    height = d['height']

    reconstructed_text = " ".join(words).strip()

    if phrase.lower() in reconstructed_text.lower():
        phrase_words = phrase.split()
        for i, w in enumerate(words):
            if phrase_words[0].lower() in w.lower():
                match = True
                for j in range(1, len(phrase_words)):
                    if i + j >= len(words) or phrase_words[j].lower() not in words[i + j].lower():
                        match = False
                        break

                if match:
                    x1, y1, w1, h1 = left[i], top[i], width[i], height[i]
                    x2, y2, w2, h2 = left[i + len(phrase_words) - 1], top[i + len(phrase_words) - 1], width[i + len(phrase_words) - 1], height[i + len(phrase_words) - 1]

                    x_left = x1
                    y_top = min(y1, y2)
                    x_right = x2 + w2
                    y_bottom = max(y1 + h1, y2 + h2)

                    return (x_left, y_top, x_right, y_bottom)

    return None
