translation_table = dict.fromkeys(map(ord, '+!@#$/'), None)

def clean_sentence_text(text):
  clean_text = text.translate(translation_table)
  if clean_text == "":
    clean_text = '...'
  return clean_text