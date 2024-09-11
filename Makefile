

tests:
	python3 tests.py 


docker-build:
	docker build -t python-datemath .

docker-run:
	docker run --rm python-datemath 

test-build: docker-build docker-run