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

	PGUSER=andyg psql -d postgres -c "TRUNCATE TABLE users, products, orders, order_items RESTART IDENTITY CASCADE;"

	env ENV=local make test
	brew services stop postgresql

push:
	# docker buildx build --platform linux/amd64 -t product-service .
	docker build -t product-service .
	docker tag product-service:latest andy2025/product-service:v5
	docker push andy2025/product-service:v5

docker_run:
	docker-compose up -d --build

minikube_run:
	env ENV=k8s kubectl apply -f ../k8s/product-service.yaml