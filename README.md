

## 📘 README (English)

🌐 Languages:
🇸🇦 [العربية](README.ar.md) | 🇺🇸 [English](README.md)

# Manga Downloader

A simple and flexible Python tool for downloading manga chapters from image-based websites and converting each chapter into a single PDF file.

---

## ✨ Features
- Sequential image downloading (one image at a time).
- Convert all chapter images into a single PDF.
- Automatic navigation to the next chapter using a configurable CSS selector.
- Reduced automation detection using:
  - Selenium
  - webdriver-manager
  - selenium-stealth

---

## 🧰 Requirements
- Python 3.8+
- Google Chrome installed
- Required packages (or use `requirements.txt`):
  - selenium
  - webdriver-manager
  - selenium-stealth
  - pillow

---

## ⚙️ Installation

### 1️⃣ Create and activate a virtual environment (Windows)
```bash
python -m venv venv
venv\Scripts\activate
````

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

or

```bash
pip install selenium webdriver-manager selenium-stealth pillow
```

---

## ▶️ Usage

1. Open the project directory.
2. Run the script:

```bash
python main.py
```

3. Provide the requested inputs:

   * First chapter URL
   * Number of chapters to download
   * CSS selector for the **Next Chapter** button
     (default: `a#next-chapter`)
   * Image URL prefix
     (example: `https://site.com/uploads`)
4. A browser window will open automatically.
   If Cloudflare appears, complete the verification manually as instructed.
5. The script will:

   * Save images into folders named `chapter_<number>`
   * Generate a PDF file named `chapter_<number>.pdf`

---

## ⚠️ Important Notes

* Make sure your usage complies with the website’s terms of service and copyright laws.
* If images fail to load:

  * Check the `image_url_prefix`
  * Or update the next chapter CSS selector.
* Some websites use aggressive anti-bot protections and may require additional adjustments.

---

## 📁 Project Structure

* `main.py` — Main entry point.
* `start_driver.py` — Chrome driver setup with stealth configuration.
* `fetch_images.py` — Image fetching and local storage.
* `images_to_pdf.py` — Converts images into PDF files.

---

## 📜 License

Use this project at your own risk and always respect content ownership and website policies.

---

