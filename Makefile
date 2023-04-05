.DEFAULT_GOAL = help

.PHONY: install-python
install-python: .venv deps  # Install Python Dependencies
	

.venv:
	test -d .venv || virtualenv .venv


.venv/.touchfile-requirements: requirements.txt
	. .venv/bin/activate; pip install -r requirements.txt
	touch $@

.PHONY: deps
deps: .venv/.touchfile-requirements
	


.PHONY: infra
infra:  # Install and run required infrastructure
	mkdir -p volumes/qdrant
	touch ./volumes/qdrant/custom_config.yaml
	docker-compose up -d

.PHONY: run
run:  # Run application
	. .venv/bin/activate; exec python main.py

.PHONY: clean
clean:  # Clean up dependencies
	rm -rf .venv || true
	find ./ -type d -name "__pycache__" -exec rm -rv {} \;

help: # Show all commands
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
