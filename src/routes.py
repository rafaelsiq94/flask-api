from flask import Blueprint, request, abort
from marshmallow import ValidationError
from sqlalchemy.orm import contains_eager
from src.models import Pai, Filho
from src.schemas import FilhoSchema, PaiSchema
from src import db

pai = Blueprint("pai", __name__)
pai_schema = PaiSchema()
filho_schema = FilhoSchema()


@pai.route("/", methods=["GET"])
def get_parents():
    query = Pai.query.all()
    json_object = pai_schema.dumps(query, many=True)
    return json_object


@pai.route("/<int:pai_id>/<int:filho_id>/", methods=["GET"])
def get_parent_and_child(pai_id, filho_id):
    pai_schema = PaiSchema()
    query = (
        Pai.query.join(Filho)
        .options(contains_eager(Pai.filhos))
        .filter(Pai.id == pai_id, Filho.id == filho_id)
        .first()
    )
    json_object = pai_schema.dumps(query, many=False)
    return json_object


@pai.route("/", methods=["POST"])
def create_parent():
    pai = request.json
    try:
        pai = pai_schema.load(pai)
    except:
        return {"errors": "erro na validação de campos"}, 422
    db.session.add(pai)
    db.session.commit()
    return pai_schema.dump(pai)


@pai.route("/<int:pai_id>/", methods=["PUT"])
def update_parent(pai_id):
    data = request.json
    filho = data.pop("filho")
    try:
        pai_schema.load(data)
        filho = filho_schema.load(filho)
    except ValidationError as err:
        return {"errors": err.messages}, 422
    old_pai = db.session.get(Pai, pai_id) or abort(404)
    old_pai.update(data)
    db.session.merge(filho)
    db.session.commit()
    return pai_schema.dumps(old_pai)


@pai.route("/<int:pai_id>", methods=["DELETE"])
def delete_parent(pai_id):
    Pai.query.filter(Pai.id == pai_id).delete()
    db.session.commit()
    return {"Message": "Parent deleted successfully"}
