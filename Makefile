.PHONY: install-python
install-python: venv deps
	

venv: .venv/.touchfile
.venv/.touchfile:
	test -d .venv || virtualenv .venv
	touch .venv/touchfile

deps: .venv/.requirements-touchfile
.venv/.requirements-touchfile:
	. .venv/bin/activate; pip install -r requirements.txt
	touch .venv/.requirements-touchfile


.PHONY: infra
infra:
	docker-compose up -d

.PHONY: run
run:
	. .venv/bin/activate; exec python main.py

.PHONY: clean
clean:
	rm -rf .venv || true
	find ./ -type d -name "__pycache__" -exec rm -rv {} \;
