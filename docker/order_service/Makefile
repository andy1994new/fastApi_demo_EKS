install:
	pip install -r requirments.txt

format:
	black *.py

lint:
	pylint *.py

test:
	pytest test.py

local_test:
	brew services start postgresql
	@echo "Waiting for PostgreSQL to initialize..."
	sleep 5

	env ENV=local make test
	brew services stop postgresql

push:
	# docker buildx build --platform linux/amd64 -t order-service .
	docker build -t order-service .
	docker tag order-service:latest andy2025/order-service:v10
	docker push andy2025/order-service:v10

docker_run:
	docker-compose up -d --build

minikube_run:
	env ENV=k8s kubectl apply -f ../k8s/order-service.yaml