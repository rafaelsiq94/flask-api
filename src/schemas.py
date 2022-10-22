from marshmallow import Schema, fields, post_load
from src.models import Pai, Filho, Professor


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

    id = fields.Integer()
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

    id = fields.Integer()
    name = fields.String(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Professor(**data)
