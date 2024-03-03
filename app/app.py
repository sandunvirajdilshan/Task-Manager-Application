from flask import Flask, render_template, request
from handler import sql_handler as sqldb


app = Flask(__name__)


# Root route Page
@app.route('/')
def index():
    return render_template('index.html')
# -----------------------------------------------------------------------------


# Get tasks route
@app.route('/tasks', methods=['GET'])
def get_tasks_route():
    if (request.method == 'GET'):
        response = sqldb.get_tasks()
        if response['success'] == 'true':
            return {
                'success': 'true',
                'tasks': response['tasks']
            }
        return {
            'success': 'false',
            'message': response['message']
        }
    return {
        'success': 'false',
        'message': 'Method Not Allowed!'
    }
# -----------------------------------------------------------------------------


# Add task route
@app.route('/addtask', methods=['POST'])
def add_task_route():
    if (request.method == 'POST'):
        data = request.form.to_dict()
        response = sqldb.add_task(data)

        if response['success'] == 'true':
            return {
                'success': 'true',
                'message': response['message']
            }        
        return {
            'success': 'false',
            'message': response['message']
        }
    return {
        'success': 'false',
        'message': 'Method Not Allowed!'
    }
# -----------------------------------------------------------------------------


# Edit task route
@app.route('/edittask', methods=['POST'])
def edit_task_route():
    if (request.method == 'POST'):
        data = request.form.to_dict()
        response = sqldb.edit_task(data)

        if response['success'] == 'true':
            return {
                'success': 'true',
                'message': response['message']
            }
        return {
            'success': 'false',
            'message': response['message']
        }
    return {
        'success': 'false',
        'message': 'Method Not Allowed!'
    }
# -----------------------------------------------------------------------------
  

# Delete task route
@app.route('/deletetask', methods=['DELETE'])
def delete_task_route():
    if (request.method == 'DELETE'):
        data = request.form.to_dict()
        response = sqldb.delete_task(data)

        if response['success'] == 'true':
            return {
                'success': 'true',
                'message': response['message']
            }
        return {
            'success': 'false',
            'message': response['message']
        }        
    return {
        'success': 'false',
        'message': 'Method Not Allowed!'
    }
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
