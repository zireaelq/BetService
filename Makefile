up: 
	docker compose --env-file ./line_provider/.env --env-file ./bet_maker/.env up -d

down: 
	docker compose --env-file ./line_provider/.env --env-file ./bet_maker/.env down

test: 
	docker compose --env-file ./line_provider/.env --env-file ./bet_maker/.env up --build

config: 
	docker compose --env-file ./line_provider/.env --env-file ./bet_maker/.env config