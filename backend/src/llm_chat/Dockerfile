FROM python:3.12.12-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y

COPY . /app/
COPY base_requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r base_requirements.txt

RUN pip install transformers
RUN pip install psycopg2-binary
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install accelerate

EXPOSE 8070

CMD ["uvicorn", "llm_service:app", "--host", "0.0.0.0", "--port", "8070"]