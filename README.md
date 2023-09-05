# Scrappy OCR Pipeline

## OCR

`ocr_images.py` uses the Google document OCR service. To use, enable the API and
create a service via https://console.cloud.google.com/. Then, log in via

```
gcloud auth application-default login
```

## AI

`parse_ocr_ai.py` requires an OpenAI API key. Create a file named `.env` in the
project root with the following fields set:

```
OPENAI_ORGANIZATION=
OPENAI_API_KEY=
```
