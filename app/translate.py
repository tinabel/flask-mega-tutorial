from app import app
from flask_babel import _
import json
import requests

def translate(text, source_language, dest_language):
  if 'MS_TRANSLATOR_KEY' not in app.config or not app.config['MS_TRANSLATOR_KEY']:
    return _('Error: the translation service is not configured.')
  auth = {
    'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY'],
    'Ocp-Apim-Subscription-Region': 'eastus',
    'Content-type': 'application/json;charset=UTF-8'
  }


  r = requests.post(
    'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}&textType=html'.format(
      source_language, dest_language
    ),
    headers=auth,
    json=text
  )

  if r.status_code != 200:
    return _('Error: the translation service failed.')

  translation_obj = []
  for translation in r.json():
    translation_obj.append(translation['translations'][0]['text'])

  return translation_obj