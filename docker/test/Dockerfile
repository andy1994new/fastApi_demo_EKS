FROM python:3.12-alpine

WORKDIR /app

COPY ./requirments.txt .
RUN pip3 install --no-cache-dir -r requirments.txt

COPY . .
CMD ["pytest"]
