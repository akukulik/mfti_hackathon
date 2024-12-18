build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

bot-up:
	docker-compose up bot -d

model-up:
	docker-compose up model -d
