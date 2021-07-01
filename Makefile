migrate:
	docker-compose run --rm web python collect_service/manage.py migrate

migrations:
	python3 collect_service/manage.py makemigrations

admin:
	python3 collect_service/manage.py createsuperuser