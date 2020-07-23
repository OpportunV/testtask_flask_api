import os

from flask import jsonify, url_for, current_app, send_file, make_response, request

from .app import db, app
from .models import Task


@app.route('/<id_>', methods=['GET'])
def get_task(id_):
    """
    :param id_: task id
    :return: either download link or the task status depending on the status
    """
    task = Task.query.filter_by(id_=id_).first()
    if not task:
        return make_response(jsonify({"error": "not found"}), 404)
    
    if task.completed:
        return jsonify({"url": url_for('download', filename=task.filename, _external=True)})
    
    return jsonify({"status": task.status})


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    """
    Opens file download window
    """
    task = Task.query.filter_by(filename=filename).first()
    if task.completed:
        return send_file(os.path.join(current_app.root_path, app.config.get('DATA_FOLDER'), filename))
    return make_response(jsonify({"error": "forbidden"}), 403)


@app.route('/add', methods=['POST'])
def add():
    """
    Adds new task with url
    :return: created task id or error
    """
    if not request.json or 'url' not in request.json:
        return make_response(jsonify({"error": "bad request"}), 400)
    
    task = Task(url=request.json['url'])
    db.session.add(task)
    db.session.commit()
    
    return jsonify({"id": task.id_})
