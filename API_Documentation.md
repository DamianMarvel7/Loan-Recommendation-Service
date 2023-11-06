# Loan Recommendation API Documentation

Welcome to the Loan Recommendation API. This document outlines the usage of various endpoints for managing customer data in the loan recommendation process.

The API is currently deployed at: https://loanrecommendationapi.azurewebsites.net/

## API Endpoints

### Read All Customers

- **URL**: `/customers`
- **Method**: `GET`
- **Description**: Retrieves a list of all customers.
- **Responses**:
  - `200 OK`: Successfully retrieved all customer data.
  - `500 Internal Server Error`: There was a problem with the server.

### Read Customer by ID

- **URL**: `/customers/{customer_id}`
- **Method**: `GET`
- **URL Params**: 
  - `customer_id=[string]`: The unique identifier of the customer.
- **Description**: Retrieves a single customer's data by their unique ID.
- **Responses**:
  - `200 OK`: Successfully retrieved the customer's data.
  - `404 Not Found`: No customer found with the provided ID.

### Add Customer

- **URL**: `/customers`
- **Method**: `POST`
- **Data Params**: JSON object containing the customer's data.
  ```json
  {
    "Customer_ID": "string",
    "Gender": "string",
    "Married": "string",
    "Dependents": "string",
    "Education": "string",
    "ApplicantIncome": "integer",
    "Property_Area": "string"
  }

- **Description**: Adds a new customer to the database.
- **Responses**:
  - `200 OK`: Successfully added the customer's data.
  - `400 Bad Request`: Customer with the same ID already exists.

### Update Customer

- **URL**: `/customers/{customer_id}`
- **Method**: `PUT`
- **URL Params**:
  - `customer_id=[string]`: The unique identifier of the customer to update.
- **Data Params**: JSON object containing the updated customer's data.
- **Description**: Updates an existing customer's data.
- **Responses**:
  - `200 OK`: Successfully updated the customer's data.
  - `400 Bad Request`: Customer with the same ID already exists.
  - `404 Not Found`: No customer found with the provided ID to update.

### Delete Customer

- **URL**: `/customers/{customer_id}`
- **Method**: `DELETE`
- **URL Params**:
  - `customer_id=[string]`: The unique identifier of the customer to delete.
- **Description**: Deletes a customer from the database.
- **Responses**:
  - `200 OK`: Successfully deleted the customer.
  - `404 Not Found`: No customer found with the provided ID to delete.

## Error Codes

- `200 OK`: The request was successful.
- `400 Bad Request`: There was an issue with the request (e.g., missing or invalid parameters).
- `404 Not Found`: The requested resource was not found.
- `500 Internal Server Error`: An error occurred on the server.