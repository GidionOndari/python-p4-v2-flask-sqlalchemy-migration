from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------- MODELS ----------
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    species = db.Column(db.String(50))

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref='employees')

# ---------- CREATE TABLES ----------
with app.app_context():
    db.create_all()

    
    if not Pet.query.first():
        pets = [Pet(name="Buddy", species="Dog"), Pet(name="Mittens", species="Cat")]
        db.session.add_all(pets)
    
    if not Department.query.first():
        departments = [Department(name="HR"), Department(name="IT")]
        db.session.add_all(departments)
    
    if not Employee.query.first():
        employees = [
            Employee(name="Alice", department_id=1),
            Employee(name="Bob", department_id=2)
        ]
        db.session.add_all(employees)
    
    db.session.commit()

# ---------- ROUTES ----------
@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask API!")

@app.route('/pets')
def get_pets():
    pets = Pet.query.all()
    return jsonify([{"id": p.id, "name": p.name, "species": p.species} for p in pets])

@app.route('/departments')
def get_departments():
    departments = Department.query.all()
    return jsonify([{"id": d.id, "name": d.name} for d in departments])

@app.route('/employees')
def get_employees():
    employees = Employee.query.all()
    return jsonify([
        {
            "id": e.id,
            "name": e.name,
            "department": e.department.name if e.department else None
        } for e in employees
    ])

if __name__ == '__main__':
    app.run(debug=True)
