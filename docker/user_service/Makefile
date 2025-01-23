install:
	pip install -r requirments.txt

format:
	black *.py

lint:
	pylint *.py

database:
	#this is only for test on local machine
	#psql postgres
	brew services start postgresql

run:
	uvicorn --host 0.0.0.0 --port 8000 main:app

test:
	#test user service

build:
	docker buildx build --platform linux/amd64 -t user-service .

push:
	docker tag user-service:latest andy2025/user-service:v1
	docker push andy2025/user-service:v1
push-ecr:
	docker tag user_service:latest 135808921973.dkr.ecr.eu-west-1.amazonaws.com/my-repository:latest
	docker push 135808921973.dkr.ecr.eu-west-1.amazonaws.com/my-repository:latest

docker_run:
	docker-compose up -d --build