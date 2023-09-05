#!/usr/bin/env python3

import json
from pathlib import Path
import pickle
import sys
from google.cloud import vision

PNG_IMAGE_DIRECTORY = 'images'
OCR_RESULTS_FILENAME = 'ocr_results.json'

client = vision.ImageAnnotatorClient()
feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

for filename in sorted(Path(PNG_IMAGE_DIRECTORY).glob('*.png')):
  print(f'loading {filename}')
  with filename.open('rb') as f:
    image = vision.Image(content=f.read())

  response = client.document_text_detection(image=image)
  response = json.loads(vision.AnnotateImageResponse.to_json(response))

  with Path(OCR_RESULTS_FILENAME).open('a') as f:
    f.write(json.dumps(response) + '\n')
