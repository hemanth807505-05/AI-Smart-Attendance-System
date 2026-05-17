from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from models.student import Student

students_bp = Blueprint('students', __name__)

@students_bp.route('', methods=['GET'])
@jwt_required()
def get_students():
    try:
        students = Student.query.all()
        return jsonify([s.to_dict() for s in students]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        return jsonify(student.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('', methods=['POST'])
@jwt_required()
def create_student():
    try:
        data = request.get_json()
        
        if not data.get('roll_number') or not data.get('name'):
            return jsonify({'error': 'Roll number and name are required'}), 400
        
        if Student.query.filter_by(roll_number=data['roll_number']).first():
            return jsonify({'error': 'Student with this roll number already exists'}), 409
        
        student = Student(
            roll_number=data['roll_number'],
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            class_name=data.get('class_name')
        )
        
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'message': 'Student created successfully',
            'student': student.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@students_bp.route('/<int:student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        
        student.name = data.get('name', student.name)
        student.email = data.get('email', student.email)
        student.phone = data.get('phone', student.phone)
        student.class_name = data.get('class_name', student.class_name)
        student.is_active = data.get('is_active', student.is_active)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Student updated successfully',
            'student': student.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@students_bp.route('/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        db.session.delete(student)
        db.session.commit()
        
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500