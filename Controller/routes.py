from flask import request, Blueprint, current_app

blueprint = Blueprint('routes', __name__, '')

@blueprint.route('/add', methods=['GET'])
def add ():
    x = request.args.get('x')
    y = request.args.get('y')
    result = current_app.celery.send_task('tasks.add_together', args=[x, y])
    r = result.get()
    print (f"Processing is {r}")
    return (f"Processing is {r}")