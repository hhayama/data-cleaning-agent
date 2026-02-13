# Makefile for data cleaning agent dashboard

.PHONY: run docker stop

run:
	@echo "Starting data cleaning agent dashboard in local mode"
	@poetry run streamlit run app.py

docker:
	@echo "Building data cleaning agent dashboard docker image"
	@docker build -t data-cleaning-agent .
	@echo " Stopping data cleaning agent dashboard docker container"
	-@docker stop data-cleaning-agent-d && docker rm data-cleaning-agent-d
	@echo "Starting data cleaning agent dashboard docker container"
	@docker run --name data-cleaning-agent-d -d -p 8501:8501 data-cleaning-agent

stop:
	@echo " Stopping data cleaning agent dashboard docker container"
	-@docker stop data-cleaning-agent-d && docker rm data-cleaning-agent-d