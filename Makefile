.PHONY: clean dist build db-dev run-dev

help:
	@echo "Allowed targets:"
	@echo "- help:    this text"
	@echo "- clean:   clean up"
	@echo "- build:   build developement container"
	@echo "- run-dev: start development container"

clean:
	rm -rf build dist py_auth_s.egg-info .coverage .coverage_html static .tox

build:
	tar cfz app.tgz --exclude=__pycache__ py_auth_s
	sudo docker build -t py_auth_s .
	rm app.tgz

run-dev:
	sudo docker run --rm -it -p 127.0.0.1:9876:9876 --name=py_auth_s py_auth_s
