import os
os.environ['DATABASE_URI'] = 'sqlite:///:memory:'
import pytest
from app import app, db
from models import StudentModel

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_post_create_form(test_client):
    response = test_client.post('/api/v1/data/create', json={
        'student_id': 1,
        'name': 'Jan Kowalski',
        'age': 23,
        'field': 'Journalism'
    }, follow_redirects=True)
    assert response.status_code == 201
    student = StudentModel.query.filter_by(student_id=1).first()
    assert student is not None
    assert student.name == 'Jan Kowalski'

def test_show_all(test_client):
    with app.app_context():
        student = StudentModel(student_id=1, name='Jan Kowalski', age=23, field='Journalism')
        db.session.add(student)
        db.session.commit()
    response = test_client.get('/api/v1/data', headers={
        'Accept': 'application/json'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'Jan Kowalski'

def test_return_id(test_client):
    with app.app_context():
        student = StudentModel(student_id=1, name='Jan Kowalski', age=23, field='Journalism')
        db.session.add(student)
        db.session.commit()
    response = test_client.get('/api/v1/data/1', headers={
        'Accept': 'application/json'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
  
def test_update_data(test_client):
    with app.app_context():
        student = StudentModel(student_id=1, name='Jan Kowalski', age=23, field='Journalism')
        db.session.add(student)
        db.session.commit()
    response = test_client.post('/api/v1/data/1/update', json={
        'name': 'Jan Kowalski',
        'age': 23,
        'field': 'IT'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert data['field'] == 'IT'

def test_delete_data(test_client):
    with app.app_context():
        student = StudentModel(student_id=1, name='Jan Kowalski', age=23, field='Journalism')
        db.session.add(student)
        db.session.commit()
    response = test_client.post('/api/v1/data/1/delete', headers={
        'Accept': 'application/json'
    })
    data = response.get_json()
    assert data['info']['message'] == 'Student with id 1 is deleted.'
    assert not data['students_list']