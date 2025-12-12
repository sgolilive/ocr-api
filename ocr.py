from io import BytesIO

import requests
import os
import pytesseract
from langdetect import detect
from PIL import Image
from logger import get_logger

os.makedirs('tessdata', exist_ok=True)
os.environ['TESSDATA_PREFIX'] = os.path.abspath('tessdata')
BASE_URL = "https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/main/"

log = get_logger('ocr')

popular_languages = [
    "eng", "fra", "deu", "spa", "ita", "por",
    "rus", "ara", "tur", "jpn", "kor",
    "chi_sim", "chi_tra", "nld", "swe", "dan",
    "fin", "nor", "pol", "ces", "hun",
    "ron", "srp", "slk", "ukr", "vie",
    "tha", "ind", "msa"
]

lang_map = {
    "en": "eng",
    "es": "spa",
    "fr": "fra",
    "de": "deu",
    "it": "ita",
    "pt": "por",
    "ru": "rus",
    "ar": "ara",
    "tr": "tur",
    "ja": "jpn",
    "ko": "kor",
    "zh-cn": "chi_sim",
    "zh-tw": "chi_tra",
    "nl": "nld",
    "sv": "swe",
    "da": "dan",
    "fi": "fin",
    "no": "nor",
    "pl": "pol",
    "cs": "ces",
    "hu": "hun",
    "ro": "ron",
    "sk": "slk",
    "sr": "srp",
    "uk": "ukr",
    "vi": "vie",
    "th": "tha",
    "id": "ind",
    "ms": "msa"
}

def _get_file_path(language):
  return f'tessdata/{language}.traineddata'

def _get_url(language):
  return f'{BASE_URL}{language}.traineddata'

def _download_trained_languages(*language):
    for lang in language:
        _download_trained_language(lang)

def _download_trained_language(language):
  filepath = _get_file_path(language)

  #if the file is already downloaded, skip it
  if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
      log.info(f'File {filepath} exists')
      return

  r = requests.get(_get_url(language), stream=True)

  if r.status_code == 200:
    with open(filepath, 'wb') as f:
      for block in r.iter_content(chunk_size = 1024):
        if block:
          f.write(block)
    log.info(f'Downloaded trained language {language}')
  else:
      log.error(f'Failed to download trained language {language}')

def _download_image(url):
    return Image.open(requests.get(url, stream=True).raw)

def _detect_language(image_data):
    _download_trained_languages('eng', 'spa', 'fra', 'deu', 'por')
    try:
        initial_text = pytesseract.image_to_string(image_data, lang="eng+spa+fra+deu+por")
        return detect(initial_text)
    except Exception as e:
        log.error(f'Failed to detect language {e}')

def process_image(image_data):

    #download image for the given url
    image = Image.open(BytesIO(image_data))

    #detect the language in the image
    detected_lang = _detect_language(image)

    #find the tess language based on the detected language
    tess_lang = lang_map.get(detected_lang, "eng")

    #download the tess language if not already downloaded
    _download_trained_language(tess_lang)

    log.info(f'detected language {detected_lang} and tesseract language {tess_lang}')

    #extract the test from the image based on the tess language
    custom_config = rf'-l {tess_lang} --oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)

    return {
        'text': text,
        'detected_lang': detected_lang,
        'tess_lang': tess_lang
    }