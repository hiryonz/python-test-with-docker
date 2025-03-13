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

    import boto3
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

@app.route('/')
def home():
    return "¡Bienvenido a la API de tareas con DynamoDB!"

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_id = str(uuid.uuid4())  # Genera un ID único
    task = {
        "task_id": task_id,
        "title": data.get("title"),
        "description": data.get("description", ""),
        "completed": False
    }
    table.put_item(Item=task)
    return jsonify({"message": "Tarea creada", "task": task}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    response = table.scan()
    return jsonify(response['Items'])

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    response = table.get_item(Key={"task_id": task_id})
    task = response.get('Item')
    if task:
        return jsonify(task)
    return jsonify({"message": "Tarea no encontrada"}), 404

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    response = table.update_item(
        Key={"task_id": task_id},
        UpdateExpression="set title=:t, description=:d, completed=:c",
        ExpressionAttributeValues={":t": data.get("title"), ":d": data.get("description"), ":c": data.get(
"completed")},
        ReturnValues="UPDATED_NEW"
    )
    return jsonify({"message": "Tarea actualizada", "updatedAttributes": response['Attributes']})

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    table.delete_item(Key={"task_id": task_id})
    return jsonify({"message": "Tarea eliminada"})