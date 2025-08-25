🚀 Overview

Investie is an AI-powered onboarding assistant built with Streamlit.
It helps first-time investors gain financial confidence by providing personalized nudges, data-driven insights, and an interactive dashboard.

Perfect 👍 thanks for clarifying! Since your prototype runs on **Streamlit**, the setup is way simpler.
Here’s a clean **README.md** tailored for judges testing a Streamlit project:

---

# 📌 Project Name: *Investie Prototype*

## 🚀 Overview

Investie is an AI-powered onboarding assistant built with **Streamlit**.
It helps first-time investors gain financial confidence by providing **personalized nudges**, **data-driven insights**, and **an interactive dashboard**.

---

## 🛠️ Installation & Setup

### 1️⃣ Clone or Download the Project

* If using **GitHub**:

  ```bash
  git clone https://github.com/your-username/investie-prototype.git
  cd investie-prototype
  ```
* Or, download the `.zip` file and extract it.

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables

Paste your API key in the **`.env` file** in the project root. Example:

```
OPENAI_API_KEY="your_api_key_here"
```

---

## ▶️ Running the Prototype

Start the Streamlit app with:

```bash
streamlit run main.py
```

* App runs locally at: **[http://localhost:8501](http://localhost:8501)**

---

## 📊 Demo Data

We included **sample CSVs** in the folder.
The prototype loads these automatically to simulate customer profiles and investment journeys.

---
