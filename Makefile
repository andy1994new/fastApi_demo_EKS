SERVICES = user_service product_service order_service

local_setup:
	sh local_evn_setup.sh

AWS_setup:
	sh eks-setup.sh

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

docker-compose-build:
	docker compose -f docker/test/docker-compose.yml up -d 

update:
	for service in $(SERVICES); do \
		sh update.sh $(VERSION) $$(echo $$service | sed 's/_service//'); \
	done