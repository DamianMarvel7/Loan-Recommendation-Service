FROM python:3.11

RUN pip install fastapi==0.104.1 uvicorn==0.23.2 pydantic==1.10.8
COPY ./App /customer
WORKDIR /customer

CMD ["uvicorn", "customer:app", "--host", "0.0.0.0", "--port", "15400"]
