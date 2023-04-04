install-python:
	virtualenv .venv
	. .venv/bin/activate; pip install -r requirements.txt

infra:
	docker-compose up -d

run:
	. .venv/bin/activate; exec python main.py

clean:
	rm -rf .venv || true
	find ./ -type d -name "__pycache__" -exec rm -rv {} \;
