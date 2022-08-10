from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from todo.resources import TaskResource, ProjectResource, TaskUpdateResource
from users.resources import UserResource, UserList


blueprint = Blueprint("todo", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(TaskResource, "/tasks", endpoint="tasks")
api.add_resource(TaskUpdateResource, "/tasks/<int:task_id>", endpoint="task_by_id")
api.add_resource(ProjectResource, "/projects", endpoint="projects")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status
    """
    return jsonify(e.messages), 400
