migrate:
	python3 collect_service/manage.py migrate && python3 collect_service/manage.py makemigrations

admin:
	python3 collect_service/manage.py createsuperuser