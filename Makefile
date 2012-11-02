.PHONY: all init clean

all: init
	python server.py

init:
	pip install -r requirements.txt

clean:
	rm -rf dist *egg*
