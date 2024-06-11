import uuid
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# referencing marshmallow
ma = Marshmallow(app)


class Product:
    def __init__(self, name):
        self.product_id = uuid.uuid4()
        self.name = name


class ProductSchema(ma.Schema):
    class Meta:
        fields = ("product_id", "name", "_links")

    # smart hyperlinking
    _links = ma.Hyperlinks(
        {"self": ma.AbsoluteURLFor("product", values=dict(product_id="<product_id>")),

         "environments": ma.AbsoluteURLFor("environments", values=dict(product_id="<product_id>")),
         "collection": ma.AbsoluteURLFor("products")}
    )


class Environment:
    def __init__(self, name, product_id):
        self.environment_id = uuid.uuid4()
        self.name = name
        self.product_id = product_id


class EnvironmentSchema(ma.Schema):
    class Meta:
        fields = ("environment_id", "product_id", "name", "_links")

    # smart hyperlinking
    _links = ma.Hyperlinks({"self": ma.AbsoluteURLFor("environment", values=dict(product_id="<product_id>",
                                                                                 environment_id="<environment_id>")),

                            "collection": ma.AbsoluteURLFor("environments", values=dict(product_id="<product_id>")),

                            "product": ma.AbsoluteURLFor("product", values=dict(product_id="<product_id>"))
                            })


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

environment_schema = EnvironmentSchema()
environments_schema = EnvironmentSchema(many=True)

PRODUCT_1 = Product("Product 1")
PRODUCT_1_ENVIRONMENTS = [
    Environment("INT", PRODUCT_1.product_id),
    Environment("STA", PRODUCT_1.product_id)]
PRODUCT_2 = Product("Product 2")
PRODUCT_2_ENVIRONMENTS = [
    Environment("INT", PRODUCT_2.product_id),
    Environment("STA", PRODUCT_2.product_id)]
PRODUCT_3 = Product("Product 3")
PRODUCT_3_ENVIRONMENTS = [
    Environment("DEV", PRODUCT_3.product_id),
    Environment("INT", PRODUCT_3.product_id),
    Environment("STA", PRODUCT_3.product_id),
    Environment("QA", PRODUCT_3.product_id)]
PRODUCT_4 = Product("Product 4")
PRODUCT_4_ENVIRONMENTS = [
    Environment("DEV", PRODUCT_3.product_id),
    Environment("QA", PRODUCT_3.product_id)]

DATA = {
    PRODUCT_1: PRODUCT_1_ENVIRONMENTS,
    PRODUCT_2: PRODUCT_2_ENVIRONMENTS,
    PRODUCT_3: PRODUCT_3_ENVIRONMENTS,
    PRODUCT_4: PRODUCT_4_ENVIRONMENTS
}


# get all products
@app.route('/api/products', methods=['GET'])
def products():
    result = products_schema.dump(DATA.keys())
    return jsonify(result)


# get a particular product
@app.route('/api/products/<product_id>', methods=['GET'])
def product(product_id):
    filtered_products = [p for p in DATA.keys() if str(p.product_id) == product_id]
    if filtered_products:
        single_product = filtered_products[0]
    else:
        return "Product not found", 404

    return product_schema.jsonify(single_product)


# get all environments
@app.route('/api/products/<product_id>/environments', methods=['GET'])
def environments(product_id):
    filtered_products = [p for p in DATA.keys() if str(p.product_id) == product_id]
    if filtered_products:
        single_product = filtered_products[0]
    else:
        return "Product not found", 404

    result = environments_schema.dump(DATA[single_product])
    return jsonify(result)


# get a particular environment
@app.route('/api/products/<product_id>/environments/<environment_id>', methods=['GET'])
def environment(product_id, environment_id):
    filtered_products = [p for p in DATA.keys() if str(p.product_id) == product_id]

    if filtered_products:
        single_product = filtered_products[0]
    else:
        return "Product not found", 404

    filtered_environments = [e for e in DATA[single_product] if str(e.environment_id) == environment_id]
    if filtered_environments:
        single_environment = filtered_environments[0]
        return environment_schema.jsonify(single_environment)
    else:
        return "Environment not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
