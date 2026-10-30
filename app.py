import logging
from flask import Flask, request, jsonify

# Configure standard logging (Experiment 12: Monitoring and Logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# In-memory student dataset
students = [
    {"id": 1, "name": "Rahul", "age": 20, "department": "CSE"},
    {"id": 2, "name": "Priya", "age": 21, "department": "CSE"}
]

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "DevOps Student REST API",
        "status": "Running",
        "version": "1.0.0",
        "endpoints": {
            "GET /students": "List all students",
            "GET /students/<id>": "Get student by ID",
            "POST /students": "Add new student",
            "PUT /students/<id>": "Update student by ID",
            "DELETE /students/<id>": "Delete student by ID",
            "GET /health": "Health check status"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "UP"}), 200

# READ all students (Exp 1, Exp 12 logging)
@app.route('/students', methods=['GET'])
def get_students():
    app.logger.info("Fetching all students. Current count: %d", len(students))
    return jsonify(students), 200

# READ one student
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    app.logger.info("Fetching student with ID: %d", id)
    for student in students:
        if student["id"] == id:
            return jsonify(student), 200

    app.logger.warning("Student with ID %d not found", id)
    return jsonify({"message": "Not found"}), 404

# CREATE student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or "name" not in data or "age" not in data or "department" not in data:
        app.logger.error("Invalid POST request payload: %s", data)
        return jsonify({"message": "Missing required fields: name, age, department"}), 400

    new_id = max([s["id"] for s in students], default=0) + 1
    student = {
        "id": new_id,
        "name": data["name"],
        "age": data["age"],
        "department": data["department"]
    }

    students.append(student)
    app.logger.info("Added new student with ID: %d (Name: %s)", new_id, student["name"])
    return jsonify(student), 201

# UPDATE student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid request body"}), 400

    for student in students:
        if student["id"] == id:
            student.update({k: v for k, v in data.items() if k != "id"})
            app.logger.info("Updated student with ID: %d", id)
            return jsonify(student), 200

    app.logger.warning("Update failed: Student with ID %d not found", id)
    return jsonify({"message": "Not found"}), 404

# DELETE student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    for student in students:
        if student["id"] == id:
            students.remove(student)
            app.logger.info("Deleted student with ID: %d", id)
            return jsonify({"message": "Deleted successfully"}), 200

    app.logger.warning("Delete failed: Student with ID %d not found", id)
    return jsonify({"message": "Not found"}), 404

if __name__ == '__main__':
    app.logger.info("Student API server starting on http://0.0.0.0:3000")
    app.run(host='0.0.0.0', port=3000, debug=True)
