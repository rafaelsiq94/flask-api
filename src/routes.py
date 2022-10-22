from flask import Blueprint, request
from sqlalchemy.orm import contains_eager
from src.models import Pai, Filho
from src.schemas import PaiSchema
from src import db

pai = Blueprint("pai", __name__)
pai_schema = PaiSchema()


@pai.route("/", methods=["GET"])
def get_parents():
    query = Pai.query.all()
    json_object = pai_schema.dumps(query, many=True)
    return json_object


@pai.route("/", methods=["POST"])
def create_parent():
    pai = request.json
    try:
        pai = pai_schema.load(pai)  # type: ignore
    except:
        return {"errors": "erro na validação de campos"}, 422
    db.session.add(pai)
    db.session.commit()
    return pai_schema.dump(pai)


@pai.route("/<int:pai_id>/", methods=["PUT"])
def update_parent(pai_id):
    data = request.json
    try:
        pai = pai_schema.load(data)  # type: ignore
    except:
        return {"errors": "erro na validação de campos"}, 422
    Pai.query.filter_by(id=pai_id).first().update(data)
    db.session.commit()
    return pai_schema.dump(pai)


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


@pai.route("/<int:pai_id>", methods=["DELETE"])
def delete_parent(pai_id):
    Pai.query.filter(Pai.id == pai_id).delete()
    db.session.commit()
    return {"Message": "Parent deleted successfully"}
