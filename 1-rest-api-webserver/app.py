from flask import Flask,render_template,request,redirect,abort,jsonify
from models import db,StudentModel
from flask_migrate import Migrate
import os
import logging
 
app = Flask(__name__)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)
 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
 
with app.app_context():
    db.create_all()
 
@app.route('/api/v1/data/create' , methods = ['GET','POST'])
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
            logging.info(f"Student {student.name} created successfully")
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
            logging.info(f"Student {student.name} created successfully")
            return redirect('/api/v1/data')

 
@app.route('/api/v1/data')
def RetrieveList():
    logging.info("GET /api/v1/data called")
    students = StudentModel.query.all()
    if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
        students_list = [
                    {
                        "id": student.id,
                        "name": student.name
                    }
                    for student in students
                ]
        logging.info(f"It could be Postman's call! Returning users: {students_list}")
        return jsonify(students_list)
    else:
        logging.info(f"Returning users: {students}")
        return render_template('datalist.html',students = students)
 
 
@app.route('/api/v1/data/<int:id>')
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
            logging.info(f"Returning student's info: {student.name}")
            return jsonify(student_info)
        else:
            logging.info(f"Returning student's info: {student.name}")
            return render_template('data.html', student = student)
    else:
        if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
            err_info = {
                "message": f"Student with id {id} does not exists"
            }
            logging.info(f"Student with id {id} does not exists")
            return jsonify(err_info)
        else:
            logging.info(f"Student with id {id} does not exists")
            return f"Student with id {id} does not exist"
 
 
@app.route('/api/v1/data/<int:id>/update',methods = ['GET','POST'])
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
                logging.info(f"Student {student.name} updated!")
                return jsonify(student_info)
            else:
                logging.info(f"Student {student.name} updated!")
                return redirect(f'/api/v1/data/{id}')
        if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
            err_info = {
                "message": f"Student with id {id} does not exists"
            }
            logging.info(f"Student with id {id} does not exists")
            return jsonify(err_info)
        else:
            logging.info(f"Student with id {id} does not exists")
            return f"Student with id {id} does not exist"
    return render_template('update.html', student = student)
 
 
@app.route('/api/v1/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            logging.info(f"Student with id {id} deleted.")
            students = StudentModel.query.all()
            if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
                info = {
                "message": f"Student with id {id} is deleted."
                }
                students_list = [
                    {
                        "id": student.id,
                        "name": student.name
                    }
                    for student in students
                ]
                return jsonify({
                    "info": info,
                    "students_list": students_list
                })
            else:
                return redirect('/api/v1/data')
        else:
            if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
                err_info = {
                "message": f"Student with id {id} does not exists"
                }
                logging.info(f"Student with id {id} does not exists")
                return jsonify(err_info)
            else:
                logging.info(f"Student with id {id} does not exists")
                abort(404)
    return render_template('delete.html')

if __name__ == "__main__":
    app.run(host='localhost', port=5000)