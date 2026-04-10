# 📸 Instagram Scraper

A Python-based automation tool built with **Playwright** to scrape data from Instagram profiles. This tool extracts profile information and post data efficiently while handling dynamic content.

---

## 🚀 Features

* **Profile Scraping:** Extract follower count, following count, and bio information
* **Data Export:** Automatically saves scraped results to `instagram_data.xlsx`
* **Session Management:** Tracks visited profiles in `visited_profiles.txt` to avoid duplicate scraping
* **Headless Mode:** Runs in the background using Playwright's browser engine

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Automation:** Playwright
* **Data Handling:** Pandas, Openpyxl
* **Environment:** Python virtual environment (venv)

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Chandan2612/instagram_scraper.git
cd instagram_scraper
```

---

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing:

```bash
pip install playwright pandas openpyxl
```

---

### 4. Install Playwright browsers

```bash
playwright install
```

---

## ▶️ Run the Script

```bash
python main.py
```

---

## 📁 Output Files

* `instagram_data.xlsx` → Scraped profile data
* `visited_profiles.txt` → Tracks already scraped profiles

---

## ⚠️ Important Notes

* Instagram may block requests if too many actions are performed quickly
* Use delays in your script to avoid detection
* Scraping should be done responsibly and ethically

---

## 🛠️ Troubleshooting

* **Playwright not working?** → Run `playwright install` again
* **Module not found?** → Reinstall dependencies
* **Script stuck?** → Check internet connection or Instagram restrictions


## 👨‍💻 Author

Chandan

---
