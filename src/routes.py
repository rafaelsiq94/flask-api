from flask import Blueprint, request
from src.models import Pai, Filho, Professor
from src.schemas import PaiSchema, FilhoSchema, ProfessorSchema
from src import db

api = Blueprint("api", __name__)
pai_schema = PaiSchema()


@api.route("/", methods=["GET"])
def get_parents():
    query = Pai.query.all()
    json_object = pai_schema.dumps(query, many=True)
    return json_object


@api.route("/", methods=["POST"])
def create_parent():
    pai = request.json
    try:
        pai = pai_schema.load(pai)  # type: ignore
    except:
        return {"errors": "erro na validação de campos"}, 422
    db.session.add(pai)
    db.session.commit()
    return pai_schema.dump(pai)


""" @app.route("/<int:pai_id>/", methods=["PUT"])
def update_parent(pai_id):
    data = request.json
    try:
        pai = PaiSchema().load(data)  # type: ignore
    except ValidationError as err:
        return {"errors": err.messages}, 422
    pai_novo = Pai.query.filter_by(id=pai_id).first().update(data)
    db.session.commit()
    return PaiSchema().dump(pai)


@app.route("/<int:pai_id>/<int:filho_id>/", methods=["GET"])
def get_parent_and_child(pai_id, filho_id):
    pai_schema = PaiSchema()
    query = (
        Pai.query.join(Filho)
        .options(contains_eager(Pai.filhos))
        .filter(Pai.id == pai_id, Filho.id == filho_id)
        .one()
    )
    json_object = pai_schema.dumps(query, many=False)
    return json_object


@app.route("/<int:pai_id>", methods=["DELETE"])
def delete_parent(pai_id):
    Pai.query.filter(Pai.id == pai_id).delete()
    db.session.commit()
    return {"Message": "Parent deleted successfully"} """
