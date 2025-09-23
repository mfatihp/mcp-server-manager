FROM python:3.12.11-bookworm


WORKDIR /app

RUN apt-get update && apt-get upgrade -y

COPY . /app/
COPY mcp_manager_core_requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r mcp_manager_core_requirements.txt

EXPOSE 8000

CMD ["uvicorn", "mcp_manager_core:core", "--host", "0.0.0.0", "--port", "8000"]