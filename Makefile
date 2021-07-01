migrate:
	docker-compose run --rm web python collect_service/manage.py migrate

migrations:
	docker-compose run --rm web python collect_service/manage.py makemigrations 

admin:
	docker-compose run --rm web python collect_service/manage.py createsuperuser 