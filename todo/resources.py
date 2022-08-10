from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from todo.schemas import TaskSchema, ProjectSchema
from users.permissions import can_edit_task
from models import Task, Project, TaskDeveloper
from extensions import db
from pagination import paginate


class TaskResource(Resource):

    method_decorators = [jwt_required()]

    def get(self):
        schema = TaskSchema(many=True)
        query = Task.query
        return paginate(query, schema)

    def post(self):
        schema = TaskSchema()
        task = schema.load(request.json)

        db.session.add(task)
        db.session.commit()

        return {"msg": "task created", "task": schema.dump(task)}, 201


class ProjectResource(Resource):

    method_decorators = [jwt_required()]

    def get(self):
        schema = ProjectSchema(many=True)
        query = Project.query
        return paginate(query, schema)

    def post(self):
        schema = ProjectSchema()
        project = schema.load(request.json)

        db.session.add(project)
        db.session.commit()

        return {"msg": "project created", "project": schema.dump(project)}, 201


class TaskUpdateResource(Resource):

    method_decorators = [jwt_required(), can_edit_task()]

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        TaskDeveloper.query.filter_by(task_id=task.id).delete()
        db.session.commit()
        db.session.delete(task)
        db.session.commit()

        return {"msg": "task deleted"}