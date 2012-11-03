.PHONY: all init clean

all: init
	python server.py 8888 1

init:
	pip install -r requirements.txt

clean:
	rm -rf dist *egg*
