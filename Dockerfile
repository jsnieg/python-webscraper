FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["fastapi", "run", "./backend/src/api/api.py", "--port", "80"]