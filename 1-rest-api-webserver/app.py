from flask import Flask,render_template,request,redirect,abort,jsonify
from models import db,StudentModel
from flask_migrate import Migrate
import os
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
 
with app.app_context():
    db.create_all()
 
@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            student_id = data['student_id']
            name = data['name']
            age = data['age']
            field = data['field']
        else:
            student_id = request.form['student_id']
            name = request.form['name']
            age = request.form['age']
            field = request.form['field']
        student = StudentModel(student_id=student_id, name=name, age=age, field = field)
        db.session.add(student)
        db.session.commit()
        if request.is_json:
            return jsonify({
                "message": "Student created successfully",
                "student": {
                    "student_id": student.student_id,
                    "name": student.name,
                    "age": student.age,
                    "field": student.field
                }
            }), 201
        else:
            return redirect('/data')

 
@app.route('/data')
def RetrieveList():
    students = StudentModel.query.all()
    if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
        students_list = [
                    {
                        "id": student.id,
                        "name": student.name
                    }
                    for student in students
                ]
        return jsonify(students_list)
    else:
        return render_template('datalist.html',students = students)
 
 
@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if student:
        if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
            student_info = {
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "field": student.field
            }
            return jsonify(student_info)
        else:        
            return render_template('data.html', student = student)
    else:
        if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
            err_info = {
                "message": f"Student with id {id} does not exists"
            }
            return jsonify(err_info)
        else:
            return f"Student with id {id} does not exist"
 
 
@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            if request.is_json:
                data = request.get_json()
                name = data['name']
                age = data['age']
                field = data['field']
            else:
                name = request.form['name']
                age = request.form['age']
                field = request.form['field']
            student = StudentModel(student_id=id, name=name, age=age, field = field)
            db.session.add(student)
            db.session.commit()
            if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
                student_info = {
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "field": student.field
                }
                return jsonify(student_info)
            else:
                return redirect(f'/data/{id}')
        if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
            err_info = {
                "message": f"Student with id {id} does not exists"
            }
            return jsonify(err_info)
        else:
            return f"Student with id {id} does not exist"
    return render_template('update.html', student = student)
 
 
@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            students = StudentModel.query.all()
            if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
                students_list = [
                    {
                        "id": student.id,
                        "name": student.name
                    }
                    for student in students
                ]
                return jsonify(students_list)
            else:
                return redirect('/data')
        else:
            if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
                err_info = {
                "message": f"Student with id {id} does not exists"
                }
                return jsonify(err_info)
            else:
                abort(404)
    return render_template('delete.html')
 
app.run(host='localhost', port=5000)