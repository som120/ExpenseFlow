# OCR Receipt Upload

## Scope delivered

- Backend OCR service using Tesseract via `pytesseract`
- Receipt upload endpoint for website: `POST /ocr/receipt`
- Telegram photo receipt processing path
- Frontend receipt upload card on Transactions page

## Current behavior

- Website users can upload an image receipt and save an inferred transaction.
- Telegram users can send a photo receipt to the bot and the bot will attempt to extract and save a transaction.
- OCR currently uses image text extraction + heuristic amount detection + existing regex transaction parsing.

## Requirements

- Server needs Tesseract OCR installed in addition to Python package dependencies.
- Best results come from clear, upright receipt images.

## Verification notes

- Python source compilation verified with `python3 -m compileall app tests`.
- OCR runtime depends on Tesseract availability in deployment environment.
