test:
	docker-compose run --rm dev python3 -m pytest

clean:
	docker-compose down

dev:
	docker-compose run --rm dev

testk:
	docker-compose run --rm dev python3 -m pytest -k $(what)
