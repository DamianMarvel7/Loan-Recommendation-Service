from fastapi import FastAPI, HTTPException
import json
from typing import Optional
from pydantic import BaseModel
import uuid

class Customer(BaseModel):
    Customer_ID: str
    Gender: str
    Married: str
    Dependents: str
    Education: str
    ApplicantIncome: int
    Property_Area: str

json_filename = "customer.json"

app = FastAPI()

def read_customer_data():
    with open(json_filename, "r") as read_file:
        data = json.load(read_file)
    return data

@app.get('/customers')
async def read_all_customers():
    data = read_customer_data()
    return data

@app.get('/customers/{customer_id}')
async def read_customer(customer_id: str):
    data = read_customer_data()
    for customer in data:
        if customer['Customer_ID'] == customer_id:
            return customer
    raise HTTPException(status_code=404, detail='Customer not found')

@app.post('/customers')
async def add_customer(customer: Customer):
    data = read_customer_data()
    customer_dict = customer.dict()
    
    # Check if Customer_ID already exists
    for existing_customer in data:
        if existing_customer['Customer_ID'] == customer_dict['Customer_ID']:
            raise HTTPException(status_code=400, detail='Customer with the same ID already exists')

    data.append(customer_dict)

    with open(json_filename, "w") as write_file:
        json.dump(data, write_file)

    return customer_dict

@app.put('/customers/{customer_id}')
async def update_customer(customer_id: str, customer: Customer):  # Change customer_id type to str
    data = read_customer_data()
    customer_dict = customer.dict()

    # Check if Customer_ID already exists
    for existing_customer in data:
        if existing_customer['Customer_ID'] == customer_dict['Customer_ID']:
            raise HTTPException(status_code=400, detail='Customer with the same ID already exists')
    
    for i, cust in enumerate(data):
        if cust['Customer_ID'] == customer_id:  # Comparing strings now
            data[i] = customer_dict
            
            with open(json_filename, "w") as write_file:
                json.dump(data, write_file)
            
            return {"message": "Customer updated.", "updated_customer": data[i]}

    raise HTTPException(status_code=404, detail='Customer not found.')

@app.delete('/customers/{customer_id}')
async def delete_customer(customer_id: str):
    data = read_customer_data()
    
    for i, customer in enumerate(data):
        if customer['Customer_ID'] == customer_id:
            data.pop(i)
            
            with open(json_filename, "w") as write_file:
                json.dump(data, write_file)
            
            return "Customer deleted."

    return "Customer not found."

