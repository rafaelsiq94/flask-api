from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import contains_eager
import os
from marshmallow import Schema, fields, ValidationError, post_load

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Pai(db.Model):  # type: ignore
    __tablename__ = "pai"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    filhos = db.relationship("Filho")

    def update(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        return self


class Filho(db.Model):  # type: ignore
    __tablename__ = "filho"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pai_id = db.Column(db.ForeignKey("pai.id", ondelete="CASCADE"))
    professores = db.relationship("Professor", secondary="filho_professor")
    pai = db.relationship("Pai")


class FilhoProfessor(db.Model):  # type: ignore
    __tablename__ = "filho_professor"

    professor_id = db.Column(
        db.ForeignKey("professor.id", ondelete="CASCADE"), primary_key=True
    )
    filho_id = db.Column(
        db.ForeignKey("filho.id", ondelete="CASCADE"), primary_key=True
    )

    professor = db.relationship("Professor")
    filho = db.relationship("Filho")


class Professor(db.Model):  # type: ignore
    __tablename__ = "professor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class PaiSchema(Schema):
    class Meta:
        model = Pai
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    filhos = fields.Nested("FilhoSchema", many=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Pai(**data)


class FilhoSchema(Schema):
    class Meta:
        model = Filho
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    pai_id = fields.Integer()
    professores = fields.Nested("ProfessorSchema", many=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Filho(**data)


class ProfessorSchema(Schema):
    class Meta:
        model = Professor
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Professor(**data)


@app.route("/", methods=["GET"])
def get_parents():
    pai_schema = PaiSchema()
    query = Pai.query.all()
    json_object = pai_schema.dumps(query, many=True)
    return json_object


@app.route("/", methods=["POST"])
def create_parent():
    pai = request.json
    try:
        pai = PaiSchema().load(pai)  # type: ignore
    except ValidationError as err:
        return {"errors": err.messages}, 422
    db.session.add(pai)
    db.session.commit()
    return PaiSchema().dump(pai)


@app.route("/<int:pai_id>/", methods=["PUT"])
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
    return {"Message": "Parent deleted successfully"}
