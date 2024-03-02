# Makefile for Supremebot

# Default target
all: setup run

# Setup environment
setup:
	pip install -r requirements.txt
	playwright install

# Run the application
run:
	poetry run streamlit run main.py

# Help command
help:
	@echo "Makefile for Supremebot"
	@echo "Available commands:"
	@echo "  all   - Setup environment, and run the application"
	@echo "  setup - Install required dependencies"
	@echo "  run   - Run the Supremebot application"
	@echo "  help  - Display this help message"

.PHONY: all clone setup run help
