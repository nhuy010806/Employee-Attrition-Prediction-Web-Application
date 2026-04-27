# 🚀 HR Attrition Prediction Web App ( One part of the project Advanced Data Analyst ) 

A full-stack AI application designed to predict the likelihood of an employee leaving the company (Attrition). This project combines a modern web interface with a robust Machine Learning model to deliver real-time HR analytics.

## ✨ Key Features
* **🤖 AI-Powered Predictions:** Utilizes a highly tuned **XGBoost Classifier** to evaluate employee data and predict turnover probability.
* **🧠 Advanced Data Processing:** Implements automated feature engineering (calculating `CommuteStress`, `PromotionDelayRatio`, etc.) and handles missing data dynamically using training set distributions.
* **⚖️ Imbalanced Data Handling:** Uses **SMOTE** (Synthetic Minority Over-sampling Technique) combined with dynamic `scale_pos_weight` to ensure accurate predictions for minority classes.
* **🎨 Modern UI/UX:** A responsive, dark-mode frontend built with React, featuring Glassmorphism effects and a clean CSS Grid layout.

## 🛠️ Tech Stack
**Frontend:**
* React.js
* HTML5 / Custom CSS (CSS Grid, Flexbox, Glassmorphism)

**Backend & Machine Learning:**
* Python / Flask / Flask-CORS
* XGBoost
* Scikit-Learn (Pipelines, Cross-validation)
* Imbalanced-Learn (SMOTE)
* Pandas / Joblib

## 📸 Screenshot
<img width="573" height="806" alt="image" src="https://github.com/user-attachments/assets/27e9265f-cf27-47f3-bccb-ad571e0d801e" />

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR-USERNAME/react-flask-hr-attrition-prediction-web.git](https://github.com/YOUR-USERNAME/react-flask-hr-attrition-prediction-web.git)
cd react-flask-hr-attrition-prediction-web
