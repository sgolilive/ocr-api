from app.ocr import process_image
from fastapi import FastAPI, HTTPException
import requests
from logger import get_logger

app = FastAPI()
log = get_logger('api')
@app.get("/")
def root():
    return {"status": "running", "message": "OCR API is live!"}

@app.get("/ocr")
async def ocr_api(url: str):

    if not url:
        log.error("No url provided")
        raise HTTPException(status_code = 400, detail='image url is required')

    try:
        response = requests.get(url, stream=True, timeout=10)
    except Exception as e:
        log.error('failed to fetch image url %s', e)
        raise HTTPException(status_code = 400, detail='failed to fetch image')

    if response.status_code != 200:
        log.error('failed to fetch image', response)
        raise HTTPException(status_code = 400, detail='failed to fetch image')

    if not response.headers.get('content-type', '').startswith('image'):
        log.error('the given url does not point to an image', response)
        raise HTTPException(status_code = 400, detail='the given url does not point to an image')

    result = process_image(response.content)

    final_response = {
        'image_url': url,
        'detected_lang': result['detected_lang'],
        'tess_language': result['tess_language'],
        'result': result['text']
    }

    log.info(final_response)

    return final_response
