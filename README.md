 # Plagiarism Detection System

## 🚀 Features
- **Anonymous two-document comparison** - No login required
- **Multi-format support**: TXT, PDF, DOCX, **Images** (JPG, PNG, BMP, TIFF via OCR)
- **Advanced algorithms**: KMP, Rabin-Karp, LCS, Cosine Similarity (TF-IDF)
- **Modern attractive UI** - Gradient themes, smooth animations, responsive design
- **Instant results** - Highlighted matches, scores, visualizations

## 📦 Quick Start (Windows)

```bash
cd d:/plagiarism-detection-system
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python app.py
```

**Open**: http://localhost:5000

## 🛠️ OCR Image Support (Optional)
For image text extraction:
1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Install & add to PATH
3. Restart terminal/VSCode

## 🔧 File Structure
```
├── app.py                 # Flask app & file parser
├── backend/
│   ├── detection.py       # Plagiarism algorithms
│   └── preprocess.py      # Text cleaning/TF-IDF
├── static/css/style.css   # Modern UI styles
├── templates/
│   ├── base.html          # Layout
│   ├── index.html         # Upload form
│   └── results.html       # Results page
├── requirements.txt       # Dependencies
└── README.md             # This file!
```

## 📊 Algorithms Used
- **KMP / Rabin-Karp**: Exact substring matches
- **LCS**: Sequence similarity
- **Cosine Similarity**: Semantic via TF-IDF vectors

## 🎨 UI Credits
- Inter & Poppins fonts (Google Fonts)
- Modern glassmorphism design
- Purple-blue gradient theme

## 🐛 Troubleshooting
- **Secret key error**: Fixed in app.py
- **Numpy import**: `pip install numpy`
- **No OCR**: Images show as unsupported (install Tesseract)
- **Port busy**: `python app.py --port=5001`

## 📈 Future Enhancements
- PDF report export
- Batch comparison
- ML-based semantic detection
- Real-time collaboration

**Built with ❤️ using Flask, NumPy, scikit-learn**

