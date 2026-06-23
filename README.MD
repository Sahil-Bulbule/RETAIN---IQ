# 📊 RetainIQ - Employee Attrition & Retention Analytics Platform

## 📌 Overview

RetainIQ is a Machine Learning-based HR Analytics platform that helps organizations analyze employee behavior, identify attrition risks, and understand workforce patterns.

The project focuses on predicting whether an employee is likely to leave the organization and provides meaningful insights related to employee retention, performance, and workplace factors.

---

## 🎯 Problem Statement

Employee attrition is a major challenge for organizations as losing skilled employees impacts productivity and business growth.

This project aims to use historical employee data to:

- Predict employee attrition risk
- Analyze factors affecting employee decisions
- Understand workforce trends
- Support HR teams with data-driven insights

---

## ✨ Features

📊 **HR Analytics Dashboard**
- Interactive employee data visualization
- Workforce trend analysis
- Department and role-based insights

🚨 **Attrition Risk Analysis**
- Identifies employees with higher exit probability
- Categorizes employees based on risk levels

📅 **Employee Behavior Analysis**
- Leave pattern analysis
- Work experience insights
- Job satisfaction evaluation

📈 **Retention Insights**
- Helps understand reasons behind employee turnover
- Provides insights for improving employee retention

🤖 **Machine Learning Prediction**
- Trained ML model for attrition prediction
- Predicts employee stay/leave probability

---

## 🧠 How It Works

RetainIQ uses an Artificial Neural Network (ANN) model to analyze employee-related factors and predict attrition risk.

The system takes employee information such as job role, income, satisfaction level, experience, overtime, and other workplace factors as input.

The data goes through preprocessing steps where categorical values are converted, features are scaled, and the processed data is passed into the ANN model.

The ANN model learns hidden patterns from historical employee data and predicts whether an employee is likely to:

- ✅ Stay in the organization
- ❌ Leave the organization

The prediction output is then displayed through an interactive HR Analytics dashboard, helping HR teams understand attrition patterns and make better retention decisions.

---

## 🛠️ Tech Stack

### Programming Language
- Python

### Data Analysis & Processing
- Pandas
- NumPy

### Machine Learning
- Scikit-Learn
- Classification Algorithms
- Model Evaluation

### Visualization
- Plotly
- Streamlit

### Model Deployment
- Joblib

### Deep Learning
- Artificial Neural Network (ANN)
- TensorFlow / Keras

---

## 🔄 Machine Learning Workflow

1. Data Collection
2. Exploratory Data Analysis (EDA)
3. Data Cleaning
4. Data Preprocessing
5. Feature Engineering
6. Model Training
7. Model Evaluation
8. Prediction Generation
9. Dashboard Deployment

---

## 📂 Project Structure
ANN PROJECT/
│
├── app.py # Streamlit Application
├── ann_model.pkl # Trained ML Model
├── an_scaler.pkl # Trained ML Model
├── ann_model.pkl # Trained ML Model
├── dataset.csv # Dataset
├── README.md # Documentation


---

## 📊 Key Factors Analyzed

The model considers various employee-related attributes:

- Age
- Department
- Job Role
- Monthly Income
- Job Satisfaction
- Work-Life Balance
- Overtime
- Years at Company
- Experience Level
- Performance Rating

---

## 📈 Model Performance

The trained model is evaluated using:

- Accuracy Score
- F1 Score
- Confusion Matrix
- Classification Report

---

## 🚀 Future Improvements

- Real-time HR analytics
- Explainable AI integration
- Advanced employee recommendation system
- Cloud deployment
- Automated HR reports

---

## 💡 Project Goal

The main goal of RetainIQ is to transform HR data into meaningful insights that help organizations make better employee retention decisions.

---

## 👨‍💻 Author

**Sahil Jain**

---

⭐ If you find this project useful, consider giving it a star!