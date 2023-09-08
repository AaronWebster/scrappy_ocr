#!/usr/bin/env python3

# Import required libraries
import json
from pathlib import Path
import re
import os
import openai
from dotenv import load_dotenv

# Define constant for OCR results filename
OCR_RESULTS_FILENAME = 'ocr_results.json'

# Load environment variables from the .env file
load_dotenv()
# Initialize OpenAI organization and API key from environment variables
openai.organization = os.getenv('OPENAI_ORGANIZATION')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the context for the GPT-4 model
context = (
    'Convert the following OCR output from a 19th century directory to JSON,'
    ' correcting any OCR errors in the process.  The fields should be "name",'
    ' "occupation", "location", and "context".  If an entry has a dash'
    ' followed by two letters, populate the "context" field with those two'
    ' letters.')

# Initialize an empty list to hold pages of OCR results
pages = []
# Read OCR results from a file and store them in the 'pages' list
with Path(OCR_RESULTS_FILENAME).open() as f:
  for line in f:
    try:
      ocr_result = json.loads(line)
      pages.append(ocr_result['fullTextAnnotation']['text'])
    except Exception as e:
      print(e)  # Print any exceptions that occur during reading

# Identify the start and end page indexes for processing
page_start = 0
page_end = 0
for page_index, page in enumerate(pages):
  if "HOUSEHOLDERS' NAMES" in page:
    page_start = page_index
  if 'INDEX TO THE REGISTER' in page:
    page_end = page_index

# Loop through the relevant pages and process them with GPT-4
for page_index in range(page_start, page_end):
  try:
    # Clean the OCR text by removing leading numbers and replacing newline characters
    cleaned_string = re.sub(r'^\d*\s', '', pages[page_index].replace('\n', ' '))
    # Send the cleaned OCR text to the GPT-4 model for further processing
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{
            'role': 'user',
            'content': context + '\n\n\n' + cleaned_string,
        }],
    )
    print(response)  # Print the response from GPT-4
    # Write the GPT-4 response to an output JSON file
    with open('output.json', 'a') as f:
      f.write(json.dumps(response) + '\n')
  except Exception as e:
    print(e)  # Print any exceptions that occur during processing
