SERVICES = user_service product_service order_service

format:
	for service in $(SERVICES); do \
		$(MAKE) -C docker/$$service format; \
	done	

lint:
	for service in $(SERVICES); do \
		$(MAKE) -C docker/$$service format; \
	done

local_test:
	brew services start postgresql
	pytest test.py