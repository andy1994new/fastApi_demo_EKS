SERVICES = user_service product_service order_service

format:
	for service in $(SERVICES); do \
		$(MAKE) -C docker/$$service format; \
	done

lint:
	for service in $(SERVICES); do \
		$(MAKE) -C docker/$$service lint; \
	done

test:
	for service in $(SERVICES); do \
		$(MAKE) -C docker/$$service test; \
	done

docker-compose-test:
	docker compose -f docker/order_service/test/docker-compose.yml up -d 
	sleep 1
	docker compose exec order-service pytest /app/test/test.py
	docker compose -f docker/order_service/test/docker-compose.yml down

update:
	for service in $(SERVICES); do \
		sh update.sh $(VERSION) $$(echo $$service | sed 's/_service//'); \
	done