FROM python:3.12.11-bookworm


WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip


COPY . .
COPY requirements_templates/base_requirements.txt .

RUN pip install --no-cache-dir -r base_requirements.txt



EXPOSE 50001

CMD ["uvicorn", "mcp:Test1", "--host", "0.0.0.0", "--port", "50001"]