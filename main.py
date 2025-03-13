from flask import Flask, request, jsonify

app = Flask(__name__)

#DB
tasks = []

@app.route('/')
def home():
    return "hola mundo"


@app.route('/task', Methods=['POST'])
def createTask():
    data = request.get_json()
    task = {
        "id": len(tasks),
        "title": data.get("title"),
        "description": data.get("description"),
        "completed": False
    }
    tasks.append(task)
    return jsonify({"message": "tarea compeltada", "task" : task}), 201



if __name__ == '__main__':
    app.run(debug=True)