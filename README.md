# ChatBot Skripsi

**A math chatbot fine-tuned with proactive conversation** designed for 8th graders with limited knowledge. Model replacement in progress (WIP).

---

## Setup

### 1. Create & Activate Virtual Environment

```bash
# Navigate to project directory
cd path/to/your/project

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the ChatBot

```bash
# Ensure virtual environment is active
# Run the Flask application
python app.py
```

Access the chatbot at `http://localhost:5000` in your browser.

---

## Dataset

* Generated datasets are located in `dataset-*.json` files.
* For a cleaner overview, see the PDF or DOCX versions in the `docs/` folder.

---

## RL Notebooks

> **Note:** GitHub cannot render notebooks with missing widget metadata.

For interactive viewing, open the following Colab links:

1. **Dataset Preparation (Binary Classification)**
   [https://colab.research.google.com/drive/175SCSH4q2zNirxzij977E8Lk-tHrbVvL?usp=sharing](https://colab.research.google.com/drive/175SCSH4q2zNirxzij977E8Lk-tHrbVvL?usp=sharing)

2. **SFT (Supervised Fine-Tuning)**
   [https://colab.research.google.com/drive/1IZiXuPi5OS\_n3xI08Wx2GH8lVs2LSf0M?usp=sharing](https://colab.research.google.com/drive/1IZiXuPi5OS_n3xI08Wx2GH8lVs2LSf0M?usp=sharing)

3. **Reward Dataset Generation**
   [https://colab.research.google.com/drive/1l2Cso\_-Gn0PWMUDIz-aNIHUUaBhOZpOf?usp=sharing](https://colab.research.google.com/drive/1l2Cso_-Gn0PWMUDIz-aNIHUUaBhOZpOf?usp=sharing)

4. **Reward Training**
   [https://colab.research.google.com/drive/1SolotV01IDfDoVXWpBH\_XSbGbPtSDVgM?usp=sharing](https://colab.research.google.com/drive/1SolotV01IDfDoVXWpBH_XSbGbPtSDVgM?usp=sharing)
