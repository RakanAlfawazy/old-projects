from App.database import Database
from App.audio import Audio
from App.model import Model
import os
from App.model import Model

class Student:
    ANSWER_TIME = 10
    RECORD_TIME = 15
    def __init__(self, student_id):
        # [student_id, username, mfcc]
        student_info = self.student_info(student_id)

        self.id = student_info[0]
        self.username = student_info[1]
        self.mfcc = student_info[2]

    @classmethod
    def get_students(cls, course_id):
        columns = ['student_id']
        conditions = {'course_id': course_id}
        student_ids = Database.fetch_all('student_course', columns, conditions)
        students = []

        for student_id in student_ids:
            students.append(Student(student_id[0]))

        return students
    @classmethod
    def validate(cls, username, password):
        
        columns = ['student_id']
        conditions = {'username': username, 'password': password}

        student_id = Database.fetch_once('students', columns, conditions)

        if not student_id:
            return False

        student_id = student_id[0]
        student = Student(student_id)
        return student

    # will return array of the specifc columns in students
    def student_info(self, student_id):
        columns = ['student_id', 'username', 'mfcc']
        conditions = {'student_id': student_id}


        student_info = Database.fetch_once('students', columns, conditions)
        return student_info

    # @classmethod
    # def record_voice(cls, username):
    #     path = f'Data/Speakers/{username}.wav'
    #     Audio.record_voice(default_time, path)
    #     return path
    @classmethod
    def answer(cls, exam_id, student_id, question_id):
        path = f'VoiceData/Answers/{exam_id}-{student_id}-{question_id}.wav'
        Audio.record_voice(cls.ANSWER_TIME, path)
        values = [None, exam_id, student_id, question_id, path, None]
        Database.insert('answers', values)
    
    @classmethod
    def play_answer(cls, question_id, student_id):
        columns = ['path']
        conditions = {'question_id': question_id, 'student_id': student_id}
        path = Database.fetch_once('answers', columns, conditions)[0]
        if path != None:
            Audio.play_voice(path)

    def submit_answers(student_id, exam_id):
        columns = ['path', 'question_id']
        conditions = {'student_id': student_id, 'exam_id': exam_id}
        rows = Database.fetch_all('answers', columns, conditions)
        mfcc = Database.fetch_once('students', ['mfcc'], {'student_id': student_id})[0]

        for row in rows: 
            path = row[0]
            question_id = row[1]
            print(path, question_id)
            print(mfcc)
            score = Model.compare_voice(mfcc, path)
            set_dict = {'score': score}
            where_dict = {'student_id': student_id, 'question_id': question_id}
            Database.update('answers', set_dict, where_dict)
    @classmethod
    def register_voice(cls, username):
        path = f'VoiceData/Training/{username}.wav'
        Audio.record_voice(cls.RECORD_TIME, path)

        return path
    @staticmethod
    def enroll(username, password, course_ids, path):
        os.path.exists(path)
        if not path:
            return None
        mfcc = Model.train_voice(path)
        values = [None, username, password, mfcc]
        Database.insert('students', values)

        student_id = Database.fetch_once('students', ['student_id'], {'username': username})[0]
        for course_id in course_ids:
            values = [student_id, course_id]
            Database.insert('student_course', values)

class Instructor:
    def __init__(self, instructor_id):
        instructor_info = self.instructor_info(instructor_id)

        self.id = instructor_info[0]
        self.username = instructor_info[1]

    def instructor_info(self, instructor_id):
        
        instructor_info = [1, 'admin', 'admin']
        return instructor_info
    
    @classmethod
    def validate(cls, username, password):

        columns = ['instructor_id']
        conditions = {'username': username, 'password': password}

        instructor_id = Database.fetch_once('instructors', columns, conditions)

        if not instructor_id:
            return False

        instructor_id = instructor_id[0]
        instructor = Instructor(instructor_id)
        return instructor
        
class admin:
    pass