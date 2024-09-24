# from flask import Flask, request, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy

# # Initialize the Flask app
# app = Flask(__name__)


# @app.route('/')

# def index():
#     return render_template('index.html')





# @app.route('/success/<int:score>')
# def success(score):
#     return "This Person has passed with " +str(score) + " marks"


# @app.route('/fail/<int:score>')
# def fail(score):
#     return "This Person failed with " + str(score) + " marks"





# @app.route('/student/<int:score>')

# def student(score):
#     if score>=35:
#         result = "This student passed"
#     elif score<35:
#         result = "This student failed"
#     return result

# books = [
#     {'id':1,"Name":"Manikanta", 'Email':"mani438@gmail.com"},
#     {'id':2,"Name":"Sruji", 'Email':"sruji@gmail.com"},
#     {'id':3,"Name":"Syamala", 'Email':"syamala@gmail.com"},
# ]

# @app.route('/books', methods = ['GET'])

# def get_books():
#     return books









# @app.route('/books/<int:book_id>', methods = ['GET'])
# def get_book(book_id):
#     for book in books:
#         if book['id'] == book_id:
#             return book
#     return {'error':'Book Not found'}


# @app.route('/create_books', methods = ['POST'])
# def create_book():
#     print("Mani")
#     new_book = {'id': len(books)+1, 'title': request.json['title'], 'author': request.json['author']}
#     books.append(new_book)
    


# if __name__=='__main__':
#     app.run(debug=True)


# ==========================================


from flask import Flask, render_template, request, redirect
from models import db, StudentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        hobbies = request.form['hobbies']
        country = request.form['country']


        students = StudentModel(

            first_name = first_name,
            last_name = last_name,
            email = email,
            password=password,
            gender=gender,
            hobbies=hobbies,
            country=country
        )

        db.session.add(students)
        db.session.commit()
        return redirect('/')

@app.route('/', methods = ['GET'])

def RetriveLists():
    students = StudentModel.query.all()
    return render_template('getstudents.html', students = students)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = StudentModel.query.get_or_404(id)

    if request.method == 'POST':
        # Update the student information from the form data
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.email = request.form['email']
        student.gender = request.form['gender']
        student.hobbies = request.form['hobbies']
        student.country = request.form['country']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating the student's information."

    # If the request is GET, render the form with the student data
    return render_template('editstudent.html', student=student)




if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(host='localhost', port=5000, debug=True)
