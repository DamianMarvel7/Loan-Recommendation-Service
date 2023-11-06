# Loan Recommendation Service

## Overview
Our Loan Recommendation Service offers a data-driven approach to assist financial institutions in extending credit to a wide range of customers. By integrating a sophisticated machine learning model, the service provides personalized loan type recommendations and default risk assessments based on individual customer data. With the aim to optimize lending processes, increase approval rates, and reduce financial risk, our platform serves as an indispensable tool for credit providers navigating the complexities of loan issuance in today’s market.

## Features
- **Machine Learning Model**: Utilizes a sophisticated algorithm to predict the likelihood of loan defaulting.
- **Recommendation System**: Advises on loan types based on a thorough analysis of customer data.
- **Customer Data API**: Facilitates CRUD operations for effective customer data management.

## Getting Started
- **Prerequisites**: Install `Python 3.11` and `pip` on your system.
- **Installation**: Run `pip install -r requirements.txt` to install all the required packages, which include FastAPI, Pydantic, and Uvicorn for the web server functionality.
- **API Usage**: Consult `API_Documentation.md` for comprehensive guidelines on interacting with the API endpoints.

## How to Install
1. Clone the repository by executing `git clone <Repository_URL>`.
2. Install the necessary Python packages with `pip install -r requirements.txt`.
3. Launch the server by running `uvicorn customer:app --reload` in your terminal.

## Details
- The machine learning model is built using XGBoost for classification tasks and OneHotEncoder for processing categorical variables.
- The loan recommendation logic provided in the `utility.py` file serves as an outline for showing how to recommend a loan.

# 18221164 - Damian Marvel
