from App.database import Database
from App.audio import Audio
class Coures:

    def __init__(self, course_id):
        course_info = self.get_course_info(course_id)
        self.id = course_info[0]
        self.name = course_info[1]
        self.instructor_id = course_info[2]

    @classmethod
    def get_student_courses(cls, student_id):
        columns = ['course_id']
        conditions = {'student_id': student_id}
        course_ids = Database.fetch_all('student_course', columns, conditions)
        courses = []
        for course_id in course_ids:
            courses.append(Coures(course_id[0]))
        
        return courses

    @classmethod
    def get_instructor_courses(cls, instructor_id):

        columns = ['course_id']
        conditions = {'instructor_id': instructor_id}
        course_ids = Database.fetch_all('courses', columns, conditions)
        courses = []
        for course_id in course_ids:
            courses.append(Coures(course_id[0]))
        
        return courses

    def get_course_info(self, course_id):
        columns = ['course_id', 'name', 'instructor_id']
        conditions = {'course_id': course_id}

        course_info = Database.fetch_once('courses', columns, conditions)
        return course_info

class Exam:

    def __init__(self, exam_id):
        exam_info = self.get_exam_info(exam_id)
        self.id = exam_info[0]
        self.name = exam_info[1]
        self.course_id = exam_info[2]

    @classmethod
    def get_exams(cls, course_id):
        columns = ['exam_id']
        conditions = {'course_id': course_id}
        exam_ids = Database.fetch_all('exams', columns, conditions)

        exams = []
        for exam_id in exam_ids:
            exams.append(Exam(exam_id[0]))
        
        return exams

    def get_exam_info(self, exam_id):
        columns = ['exam_id', 'name', 'course_id']
        conditions = {'exam_id': exam_id}

        exam_info = Database.fetch_once('exams', columns, conditions)
        return exam_info

class Question:

    def __init__(self, question_id):
        question_info = self.get_question_info(question_id)
        self.id = question_info[0]
        self.question = question_info[1]
        self.exam_id = question_info[2]

    @classmethod
    def get_questions(cls, exam_id):
        columns = ['question_id']
        conditions = {'exam_id': exam_id}
        question_ids = Database.fetch_all('questions', columns, conditions)
        questions = []

        for question_id in question_ids:
            questions.append(Question(question_id[0]))
        
        return questions

    def get_question_info(self, question_id):
        columns = ['question_id', 'question', 'exam_id']
        conditions = {'question_id': question_id}

        question_info = Database.fetch_once('questions', columns, conditions)
        return question_info

class Answer:

    def __init__(self, answer_id):
        answer_info = self.get_answer_info(answer_id)
        self.id = answer_info[0]
        self.question_id = answer_info[1]
        self.exam_id = answer_info[2]
        self.student_id = answer_info[3]
        self.path = answer_info[4]
        self.score = answer_info[5]

    @classmethod
    def get_answers(cls, student_id, exam_id):
        columns = ['answer_id']
        conditions = {'student_id': student_id, 'exam_id': exam_id}
        answer_ids = Database.fetch_all('answers', columns, conditions)

        answers = []
        for answer_id in answer_ids:
            answers.append(Answer(answer_id[0]))
        
        return answers

    def get_answer_info(self, answer_id):

        conditions = {'answer_id': answer_id}

        answer_info = Database.fetch_once('answers', conditions=conditions)
        return answer_info

    def play(self):
        Audio.play_voice(self.path)