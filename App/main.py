from fastapi import FastAPI,Request
from customer import app as customer_router
from auth import router as auth_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(customer_router)
