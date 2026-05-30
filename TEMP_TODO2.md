TODO - PDF/DOCX parsing fix

- [ ] Reproduce issue by adding debug to parse_file to log extracted length
- [ ] Improve PDF parsing: use page.get_text("text") and strip; handle empty text
- [ ] Improve DOCX parsing: include tables and headers/footers if present
- [ ] Add fallback: if parsed text is empty, try OCR for PDFs/images (optional)
- [ ] Add server-side error details back to UI (flash) for easier debugging

