# ChatBot Skripsi

**A math chatbot fine-tuned with proactive conversation** designed for 8th graders with limited knowledge. Model replacement in progress (WIP).

> **Note:** As you can see, generated-responses.json is not same as final_reward_dataset.json, it is caused by missing file while development. But the dataset used for training is final_reward_dataset.json. So the generated-response.json doesn't matter much. You can generate it using notebook no 3 and the to generate final_reward_dataset you need to run Helpers/rewardDatasetMaker.py

---

## Setup

### 1. Create & Activate Virtual Environment

```bash
cd path/to/your/project

# Create venv
python -m venv venv

# Activate venv
.\venv\Scripts\activate

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the ChatBot

```bash
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

1. **Training using paper method (Binary Classification)**
> **Note:** This trained model didn't work well so head over to link number 2 to see the SFT part
   [https://colab.research.google.com/drive/175SCSH4q2zNirxzij977E8Lk-tHrbVvL?usp=sharing](https://colab.research.google.com/drive/175SCSH4q2zNirxzij977E8Lk-tHrbVvL?usp=sharing)


2. **SFT (Supervised Fine-Tuning)**
   [https://colab.research.google.com/drive/1IZiXuPi5OS\_n3xI08Wx2GH8lVs2LSf0M?usp=sharing](https://colab.research.google.com/drive/1IZiXuPi5OS_n3xI08Wx2GH8lVs2LSf0M?usp=sharing)

3. **Reward Dataset Generation**
   [https://colab.research.google.com/drive/1l2Cso\_-Gn0PWMUDIz-aNIHUUaBhOZpOf?usp=sharing](https://colab.research.google.com/drive/1l2Cso_-Gn0PWMUDIz-aNIHUUaBhOZpOf?usp=sharing)

4. **Reward Training**
   [https://colab.research.google.com/drive/1SolotV01IDfDoVXWpBH\_XSbGbPtSDVgM?usp=sharing](https://colab.research.google.com/drive/1SolotV01IDfDoVXWpBH_XSbGbPtSDVgM?usp=sharing)
