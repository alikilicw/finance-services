#cnga1dhr01qq9hn8s180cnga1dhr01qq9hn8s18g   finhub token

def text_convert(text):
    text = text.lstrip()
    text = str(text).replace(' ', '_')

    turkish_characters = "çÇğĞıİöÖşŞüÜ"
    english_characters = "cCgGiIoOsSuU"

    translate_table = str.maketrans(turkish_characters, english_characters)
    text = text.translate(translate_table)

    text = text.lower()
    return text