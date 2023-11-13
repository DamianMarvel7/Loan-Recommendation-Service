from fastapi import  Depends, status, HTTPException, APIRouter
import json
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated
from Utility.utils import  encode_token, decode_token, hash_password,verify_password
from Utility.Model.model import get_customer, recommend_loan
import pandas as pd
class Customer(BaseModel):
    Customer_ID: str
    Gender: str
    Married: str
    Dependents: str
    Education: str
    ApplicantIncome: int
    Property_Area: str
    Username: str
    


app = APIRouter()


json_filename = "customer.json"
json_userfilename = "user.json"



def read_account_data():
    
    with open(json_userfilename, "r") as read_file:
        data = json.load(read_file)
    return data


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# Example of how to decode a token and get the user
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
    users_db = read_account_data()
    
    user = get_user(users_db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def read_customer_data(current_user: User = Depends(get_current_active_user)):
    # Current user is authenticated at this point
    with open(json_filename, "r") as read_file:
        data = json.load(read_file)
    return data

@app.get('/customers')
async def read_all_customers(current_user: User = Depends(get_current_active_user)):
    # Check if the user is "admin" and password is "secret"
    if current_user.username != "admin" or not verify_password("secret", current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

    data = read_customer_data(current_user=current_user)
    return data

@app.get('/customers/{customer_id}')
async def read_customer(customer_id: str, current_user: User = Depends(get_current_active_user)):
    data = read_customer_data()
    for customer in data:
        if customer['Customer_ID'] == customer_id:
            print(current_user)
            if customer['Username'] == current_user.username:
                return customer
            else:
                raise HTTPException(status_code=403, detail="Access denied")
    raise HTTPException(status_code=404, detail='Customer not found')

@app.post('/customers')
async def add_customer(customer: Customer, current_user: User = Depends(get_current_active_user)):
    data = read_customer_data()
    customer_dict = customer.dict()
    customer_dict['Username'] = current_user.username  # Set owner

    # Check if Customer_ID or Username already exists
    existing_ids = {cust['Customer_ID'] for cust in data}
    existing_usernames = {cust['Username'] for cust in data}
    if customer_dict['Customer_ID'] in existing_ids:
        return {"error": "Customer_ID already exists."}
    if customer_dict['Username'] in existing_usernames:
        return {"error": "Username already exists."}

    data.append(customer_dict)

    with open(json_filename, "w") as write_file:
        json.dump(data, write_file)

    return customer_dict

@app.put('/customers/{customer_id}')
async def update_customer(customer_id: str, customer: Customer, current_user: User = Depends(get_current_active_user)):
    data = read_customer_data()

    for i, cust in enumerate(data):
        if cust['Customer_ID'] == customer_id:
            if cust['Username'] == current_user.username:
                # Check if the 'Customer_ID' or 'Username' fields are being changed
                if customer.Customer_ID != cust['Customer_ID'] or customer.Username != cust['Username']:
                    raise HTTPException(status_code=400, detail="Customer ID and Username cannot be changed")

                # Remove the 'Customer_ID' field from the customer_dict to prevent changes
                customer_dict = customer.dict(exclude={'Customer_ID'})

                data[i].update(customer_dict)  # Update the existing customer data
                with open(json_filename, "w") as write_file:
                    json.dump(data, write_file)
                return {"message": "Customer updated.", "updated_customer": data[i]}
            else:
                raise HTTPException(status_code=403, detail="Access denied")

    raise HTTPException(status_code=404, detail='Customer not found.')

@app.delete('/customers/{customer_id}')
async def delete_customer(customer_id: str, current_user: User = Depends(get_current_active_user)):
    data = read_customer_data()
    
    for i, customer in enumerate(data):
        if customer['Customer_ID'] == customer_id:
            if customer['Username'] == current_user.username:
                data.pop(i)
                with open(json_filename, "w") as write_file:
                    json.dump(data, write_file)
                return "Customer deleted."
            else:
                raise HTTPException(status_code=403, detail="Access denied")

    raise HTTPException(status_code=404, detail="Customer not found.")

def get_customer_internal(customer_id, loan_amount, loan_amount_term):
    data = read_customer_data()  # Make sure this function returns a list of customers
    for customer in data:
        if customer['Customer_ID'] == customer_id:
            customer['LoanAmount'] = float(loan_amount)
            customer['Loan_Amount_Term'] = float(loan_amount_term)
            df = pd.DataFrame([customer])
            df = df[['Gender', 'Married', 'Dependents', 'Education', 'ApplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Property_Area']]
            return df
    return None

class LoanRequest(BaseModel):
    loan_amount: int
    loan_amount_term: int


@app.post('/recommend_loan/{customer_id}')
async def recommend_loan_api(customer_id: str, loan_request: LoanRequest, current_user: User = Depends(get_current_active_user)):
    # Your existing authorization logic here...

    # Fetch customer data
    customer_data = get_customer_internal(customer_id, loan_request.loan_amount, loan_request.loan_amount_term)
    if customer_data is None:
        raise HTTPException(status_code=404, detail="Customer not found or error in fetching data.")

    # Make the loan recommendation
    recommendation = recommend_loan(customer_data)

    return recommendation