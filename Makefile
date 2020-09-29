build:
	export FLASK_APP=restApi
	export FLASK_ENV=development
run:
	@echo "Rodando flask" 
	python3 restApi.py