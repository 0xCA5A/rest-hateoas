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
	curl -X GET http://localhost:5000/api/products?links=true -H "Content-Type:application/hal+json; charset=utf-8" -v  -d "{}"

clean:
	rm -rf venv
