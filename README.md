# Proactive Math ChatBot Final Project

**A math chatbot fine-tuned with proactive conversation** designed for 8th graders with limited knowledge. Model replacement in progress (WIP).

> **Note:** As you can see, generated-responses.json is not same as final_reward_dataset.json, it is caused by missing file while development. But the dataset used for training is final_reward_dataset.json. So the generated-response.json doesn't matter much. You can generate it using notebook no 3 to generate final_reward_dataset you need to run Helpers/rewardDatasetMaker.py

> Highly referenced HF blog about RLHF, on this blog https://huggingface.co/blog/stackllama 

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

## Fine-tune files
[https://drive.google.com/drive/folders/1_J-PrgrJ_PrbY2DbPGK2Dz5w7gZOriCr](https://drive.google.com/drive/folders/1_J-PrgrJ_PrbY2DbPGK2Dz5w7gZOriCr)

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

5.**PPO Training**
   > **Note:** Several notebooks are used for ppo training since TRL 16 has an error in PPO .step method, the solution is to downgrade the TRL library to 0.11.0, that suits well with this project. Different notebook indicates different apporach in hyperparameter tuning, dataset, and base trained model.
   [https://colab.research.google.com/drive/16L-Y3Ep5nElfvNP0yQyGkLdXcVrxC2xB?usp=sharing](https://colab.research.google.com/drive/16L-Y3Ep5nElfvNP0yQyGkLdXcVrxC2xB?usp=sharing)
   [https://colab.research.google.com/drive/1vZs2TMpw2VGdQNUJEw4hr-e8CQoSlOz5?usp=sharing](https://colab.research.google.com/drive/1vZs2TMpw2VGdQNUJEw4hr-e8CQoSlOz5?usp=sharing)

6.**Evaluation Script**
   [https://colab.research.google.com/drive/1NxqJjuIelzzoqtlDNxvvhOAU_yDiCxWQ](https://colab.research.google.com/drive/1NxqJjuIelzzoqtlDNxvvhOAU_yDiCxWQ?usp=sharing)

7.**Deployment Script**
   [https://colab.research.google.com/drive/1mDuDIV6byBbOwv7BquD6Yjrm6UEXlBsD?usp=sharing](https://colab.research.google.com/drive/1mDuDIV6byBbOwv7BquD6Yjrm6UEXlBsD?usp=sharing)
