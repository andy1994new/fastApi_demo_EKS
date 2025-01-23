FROM python:3.12-alpine

WORKDIR /app

COPY ./requirments.txt .
RUN pip3 install --no-cache-dir -r requirments.txt

EXPOSE 8000

COPY . .
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
