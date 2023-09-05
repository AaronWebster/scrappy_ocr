import json
from pathlib import Path
import re
import openai
from dotenv import load_dotenv

OCR_RESULTS_FILENAME = 'ocr_results.json'

# Create a file named '.env' with the following environment variables.
load_dotenv()
openai.organization = os.getenv('OPENAI_ORGANIZATION')
openai.api_key = os.getenv('OPENAI_API_KEY')

context = (
    'Convert the following OCR output from a 19th century directory to JSON,'
    ' correcting any OCR errors in the process.  The fields should be "name",'
    ' "occupation", "location", and "context".  If an entry has a dash'
    ' followed by two letters, populate the "context" field with those two'
    ' letters.')

pages = []
with Path(OCR_RESULTS_FILENAME).open() as f:
  for line in f:
    try:
      ocr_result = json.loads(line)
      pages.append(ocr_result['fullTextAnnotation']['text'])
    except Exception as e:
      print(e)

page_start = 0
page_end = 0
for page_index, page in enumerate(pages):
  if "HOUSEHOLDERS' NAMES" in page:
    page_start = page_index
  if 'INDEX TO THE REGISTER' in page:
    page_end = page_index

for page_index in range(page_start, page_end):
  try:
    cleaned_string = re.sub(r'^\d*\s', '', pages[i].replace('\n', ' '))
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{
            'role': 'user',
            'content': context + '\n\n\n' + cleaned_string,
        }],
    )
    print(response)
    with open('output.json', 'a') as f:
      f.write(json.dumps(response) + '\n')
  except Exception as e:
    print(e)
