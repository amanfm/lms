from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)

database_name = "school"
DB_URI = "mongodb+srv://m001-student:m001-mongodb-basics@sandbox.j0jwd.mongodb.net/school?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)


@app.route('/')
def hello_world():
    return 'Welcome to Learning Management System'


class Detail(db.Document):
    student_id = db.IntField()
    program = db.StringField()
    semester = db.IntField()
    course = db.StringField()
    section = db.StringField()
    instructor = db.StringField()

    def to_json(self):
        return {
            "student_id": self.program,
            "program": self.program,
            "semester": self.semester,
            "course": self.course,
            "section": self.section,
            "instructor": self.instructor
        }


@app.route('/populate', methods=['POST'])
def db_populate():
    detail1 = Detail(student_id=1, program="BE", semester=1, course="Maths", section="A", instructor="Deepak")
    detail2 = Detail(student_id=2, program="BBA", semester=1, course="account", section="B", instructor="Gagan")
    detail3 = Detail(student_id=3, program="BIM", semester=1, course="tours", section="A", instructor="Pretna")
    detail1.save()
    detail2.save()
    detail3.save()
    return make_response("", 201)


@app.route('/api/student', methods=['GET', 'POST'])
def api_student():
    if request.method == "GET":
        details = []
        for detail in Detail.objects:
            details.append(detail)
        return make_response(jsonify(details), 200)
    elif request.method == "POST":
        content = request.json
        detail = Detail(student_id=content['student_id'],
                        program=content['program'], semester=content['semester'], course=content['course'],
                        section=content['section'], instructor=content['instructor'])
        detail.save()
        return make_response("", 201)


@app.route('/api/semester/<semester>', methods=['GET'])
def api_each_semester(semester):
    if request.method == "GET":
        result = Detail.objects(semester=semester)
        return result.to_json()


@app.route('/api/program/<program>', methods=['GET'])
def api_each_program(program):
    if request.method == "GET":
        result1 = Detail.objects(program=program)
        return result1.to_json()


@app.route('/api/course/<course>', methods=['GET'])
def api_each_course(course):
    if request.method == "GET":
        result2 = Detail.objects(course=course)
        return result2.to_json()

    

if __name__ == '__main__':
    app.run()
