FROM python:3.11

COPY Pipfile ./
COPY Pipfile.lock ./

RUN apt-get update && apt-get -y install libgl1-mesa-glx
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /app

COPY main.py /app
COPY ETF_Functions.py /app
COPY backtesting_engine.py /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"] 