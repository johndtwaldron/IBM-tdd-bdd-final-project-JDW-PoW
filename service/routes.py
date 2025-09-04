######################################################################
# Copyright 2016, 2022 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# spell: ignore Rofrano jsonify restx dbname
"""
Product Store Service with UI
"""
from flask import jsonify, request, abort
from flask import url_for  # noqa: F401 pylint: disable=unused-import
from service.models import Product, Category
from service.common import status  # HTTP Status Codes
from . import app


######################################################################
# H E A L T H   C H E C K
######################################################################
@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="OK"), status.HTTP_200_OK


######################################################################
# H O M E   P A G E
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# C R E A T E   A   N E W   P R O D U C T
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to Create a Product...")
    check_content_type("application/json")
    # ensure JSON
    if not request.is_json:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be application/json")

    data = request.get_json()
    app.logger.info("Processing: %s", data)
    product = Product()
    product.deserialize(data)
    product.create()
# app.logger.info("Product with new id [%s] saved!", product.id)
    app.logger.info("Created product %s", product.name)

# message = product.serialize()

    #
    # Uncomment this line of code once you implement READ A PRODUCT
    #
    location_url = url_for("get_products", product_id=product.id, _external=True)
    return jsonify(product.serialize()), status.HTTP_201_CREATED, {"Location": location_url}
    # return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# L I S T   A L L   P R O D U C T S
######################################################################

@app.route("/products", methods=["GET"])
def list_products():
    """
    List Products (optionally filtered by ?name=, ?category=, ?available=)
    """
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        # will raise if invalid; if you want to be nicer:
        #   try: cat = getattr(Category, category.upper())
        #   except AttributeError: abort(status.HTTP_400_BAD_REQUEST, "Invalid category")
        cat = getattr(Category, category.upper())
        products = Product.find_by_category(cat)
    elif available is not None:
        products = Product.find_by_availability(_str2bool(available))
    else:
        products = Product.all()

    return [p.serialize() for p in products], status.HTTP_200_OK


######################################################################
# READ A PRODUCT
######################################################################

@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product

    This endpoint will return a Product based on it's id
    """
    app.logger.info("Request to Retrieve a product with id [%s]", product_id)

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    app.logger.info("Returning product: %s", product.name)
    return product.serialize(), status.HTTP_200_OK


######################################################################
# U P D A T E   A   P R O D U C T
######################################################################


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product by id
    """
    app.logger.info("Request to Update product with id [%s]", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    data = request.get_json() or {}

    # Normalize 'available' (UI may send a string)
    if "available" in data and isinstance(data["available"], str):
        data["available"] = data["available"].strip().lower() in ("true", "1", "yes", "y")

    # Normalize/ensure 'category'
    if "category" in data:
        if isinstance(data["category"], str) and data["category"]:
            data["category"] = data["category"].upper()  # e.g., "Cloths" -> "CLOTHS"
        else:
            data["category"] = product.category.name
    else:
        data["category"] = product.category.name

    # Ensure name isn’t dropped
    if not data.get("name"):
        data["name"] = product.name

    product.deserialize(data)
    product.id = product_id
    product.update()
    return product.serialize(), status.HTTP_200_OK


######################################################################
# D E L E T E   A   P R O D U C T
######################################################################


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product by id
    """
    app.logger.info("Request to Delete product with id [%s]", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    product.delete()
    return "", status.HTTP_204_NO_CONTENT

######################################################################
# extra
######################################################################


def _str2bool(val: str):
    if isinstance(val, bool):
        return val
    if val is None:
        return None
    return val.strip().lower() in ("true", "1", "yes", "y")
