from app import db
from app.models.productcategory import ProductCategory
from app.schemas.productcategory_schema import productcategory_schema
from flask import Blueprint, Flask, jsonify, request


bp = Blueprint('productcategory', __name__, url_prefix='/api/v1/productcategory')

@bp.route('/', methods=['GET'])
def get_productcategories():
    """Get all productcategories"""
    query = ProductCategory.query.all()
    result = productcategory_schema.dump(query, many=True)

    return {"productcategories" : result.data}

@bp.route('/<int:productcategoryid>', methods=['GET'])
def get_productcategory(productcategoryid):
    """Get a productcategory by id"""
    query = ProductCategory.query.get_or_404(productcategoryid)
    result = productcategory_schema.dump(query)

    return result.data

@bp.route('/', methods=['POST'])
def create_productcategory():
    """Create a new productcategory """
    json_data = request.get_json()

    if not json_data:
        return "No data provided", 404

    # Validate and deserialize input
    deserialize_result = productcategory_schema.load(json_data)
    if (any(deserialize_result.errors)):
        return deserialize_result.errors, 400

    new_productcategory = deserialize_result.data

    db.session.add(new_productcategory)
    db.session.commit()
    result = productcategory_schema.dump(ProductCategory.query.get(new_productcategory.id))
   
    return result.data, 201

@bp.route('/<int:productcategoryid>', methods=['PUT'])
def update_productcategory(productcategoryid):
    """Update an existing productcategory """
    productcategory = ProductCategory.query.get_or_404(productcategoryid)
    json_data = request.get_json()

    if not json_data:
        return "No data provided", 404

    # Validate and deserialize input
    deserialize_result = productcategory_schema.load(json_data)
    if (any(deserialize_result.errors)):
        return deserialize_result.errors

    new_productcategory = deserialize_result.data

    productcategory.name = new_productcategory.name

    db.session.commit()

    return productcategory_schema.dump(productcategory).data, 201

@bp.route('/<int:productcategoryid>', methods=['DELETE'])
def delete_productcategory(productcategoryid):
    """Delete a productcategory by id"""
    query = ProductCategory.query.get_or_404(productcategoryid)

    db.session.delete(query)
    db.session.commit()

    return '', 200
