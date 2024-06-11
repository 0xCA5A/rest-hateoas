default: run

init:
	python3 -m venv venv

install:
	venv/bin/pip install -r requirements.txt

freeze:
	venv/bin/pip freeze > requirements.txt

run:
	venv/bin/python3 app.py

test:
	curl http://127.0.0.1:5000/api/products -H "Content-Type:application/json; charset=utf-8" -v

container:
	docker build -t localhost/rest-hateoas:latest .

container_run:
	docker run -p 5000:5000 localhost/rest-hateoas:latest

container_test:
	curl http://127.0.0.1:5000/api/products -H "Content-Type:application/json; charset=utf-8" -v


clean:
	rm -rf venv
