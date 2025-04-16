
# Notes to track the project

- [x] A good and reliable pdf-to-text parser: `pymupdf` ( python ) and poppler's `pdftotext` (debian util)
     - pdftotext is better now, since we can convert pdfs to text in bulk by using `xargs` ( ~52.1 pdfs converted per second with 8 workers ) but does not support all types of pdfs
     - pymupdf is better for quality, since it makes use of `tessaract` OCR but very slow ( ~20 mins to convert 100 pdfs )
- [x] A backend for our **embedding model**
- [ ] A backend for our **summarizer model**
- [ ] A **meta-data database** to lookup papers
- [ ] A bulk **pdf** database ( in filesystem or a DB, whichever is faster in retrieval)
- [ ] A Vector DB, simple, light and fast
- [ ] A script to finetune (a) embedding model, and (b) summarizer model.
- [ ] ML-Flow dashboards, a repository to store models, and a ray cluster.
- [ ] ... etc

