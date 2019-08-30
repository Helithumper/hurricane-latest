#!make
include .env
export $(shell sed 's/=.*//' .env)

deploy:
	serverless deploy --aws-s3-accelerate

invoke-graphic:
	serverless invoke -f get_latest_graphic_and_post

invoke-report:
	serverless invoke -f get_latest_report_and_post

test-local:
	@python3 handler.py

test-utilities:
	@python3 utilities.py

test-noaa:
	@python3 noaa.py

.PHONY: deploy invoke test-local test-utilities
