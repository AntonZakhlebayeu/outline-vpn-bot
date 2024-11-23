IMAGE_NAME=outline-vpn-bot

build-clear:
	docker build --no-cache -t $(IMAGE_NAME) -f docker/Dockerfile .

build:
	mv .dockerignore .dockerignore.backup
	docker build --no-cache -t $(IMAGE_NAME) -f docker/Dockerfile .
	mv .dockerignore.backup .dockerignore
	
run:
	docker run --name $(IMAGE_NAME) $(IMAGE_NAME)

start:
	docker start $(IMAGE_NAME)

stop: 
	docker stop $(IMAGE_NAME)

remove:
	docker rm $(IMAGE_NAME)

build-and-run: build run
