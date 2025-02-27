build-docker:
	uv pip compile pyproject.toml -o backend/requirements.txt && \
	docker compose -f docker-compose.yml build
up:
	docker compose -f docker-compose.yml up -d
down:
	docker compose -f docker-compose.yml down

test:
	# docker compose -f docker-compose.yml run tests
	docker compose -f docker-compose.yml --profile test up -d
