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
	cd docker/test
	docker compose up -d
	sleep 5
	docker compose  exec user-service pytest test.py
	docker compose down

update:
	for service in $(SERVICES); do \
		sh update.sh $(VERSION) $$(echo $$service | sed 's/_service//'); \
	done