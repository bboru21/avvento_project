.POSIX:

VENV=venv

.PHONY: help
help:
	@echo 'help'

update:
	( \
		source $(VENV)/bin/activate; \
		pip install --upgrade pip; \
		pip install -r requirements.txt; \
		deactivate; \
	)

.PHONY: serve
serve:
	$(VENV)/bin/python3 avvento/manage.py runserver 0.0.0.0:9000 --settings avvento.settings.local
