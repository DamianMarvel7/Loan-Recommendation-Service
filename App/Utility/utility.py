import requests
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import joblib

def transform_customer_data(df):
    columns_to_encode = ['Gender', 'Married', 'Education', 'Property_Area']

    preprocessor = joblib.load('./App/Utility/preprocessor.joblib')
    df_encoded_array = preprocessor.transform(df)
    feature_names = (preprocessor.named_transformers_['one_hot'].get_feature_names_out(columns_to_encode)
                    .tolist() + [col for col in df.columns if col not in columns_to_encode])

    df_encoded = pd.DataFrame(df_encoded_array, columns=feature_names)
    df_encoded = df_encoded.astype(int)

    return df_encoded

def get_customer(customer_id,loan_amount,loan_amount_term):
    api_url = f"https://loanrecommendationapi.azurewebsites.net/customers/{customer_id}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        # Successfully retrieved data
        data = response.json()
        df = pd.DataFrame([data])
        df['LoanAmount'] = loan_amount
        df['Loan_Amount_Term'] = loan_amount_term

        # Select only the required columns
        df = df[['Gender', 'Married', 'Dependents', 'Education', 'ApplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Property_Area']]
        return df
    else:
        # Handle error
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(response.text)

def predict_default(df):
    df_preprocessed = transform_customer_data(df)
    model = joblib.load('./App/Utility/xgb_model.joblib')
    pred = model.predict(df_preprocessed)

    if(pred==0):
        return 'Default'
    else:
        return 'Not Default'

import pandas as pd

def predict_loan_type(data):
    # Sample logic to recommend loan type
    if data["ApplicantIncome"].values[0] > 5000:
        loan_type = "Short Term"
        interest_rate = 3.0
        loan_term = data['Loan_Amount_Term'].values[0]
    else:
        loan_type = "Long Term"
        interest_rate = 5.0
        loan_term = data['Loan_Amount_Term'].values[0]*1.2
        
    # Sample logic to predict default
    if(predict_default(data)=='Default'):
        loan_amount = data['LoanAmount'].values[0]*0.8
    else:
        loan_amount = data['LoanAmount'].values[0]
    print(loan_type, interest_rate, loan_term, loan_amount)
    
    return loan_type, interest_rate, loan_term, loan_amount

def recommend_loan(data):
    # Predict loan type and default risk
    loan_type, interest_rate, loan_term, loan_amount = predict_loan_type(data)

    # Return the result
    return {
        "LoanType": loan_type,
        "InterestRate": interest_rate,
        "TenureMonths": loan_term,
        "WillDefault": loan_amount
    }

# Example usage:
customer_id = "1"
customer_data  = get_customer(customer_id,110,360)
print(customer_data['Gender'].values[0])
print(predict_default(customer_data))

print(recommend_loan(customer_data))