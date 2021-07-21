migrate:
	docker-compose run --rm web python manage.py migrate

migrations:
	docker-compose run --rm web python manage.py makemigrations 

admin:
	docker-compose run --rm web python manage.py createsuperuser 

test:
	docker-compose run --rm web pytest

sqlprint:
	docker-compose run --rm web python manage.py shell_plus --print-sql

import:
	docker-compose run --rm web python manage.py csv_import