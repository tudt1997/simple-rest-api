# Simple REST API

A simple REST API with 2 endpoints:

`/insert-pool`: Insert or append values to a pool

`/calculate-quantile`: Calculate the quantile of a pool

## Requirements

Python 3.6+

## Installation

`pip install -r requirements.txt`

## Run the server

`uvicorn main:app --reload`

## Interactive API docs

When the server is running, go to http://127.0.0.1:8000/docs.

## Run test

`pytest`