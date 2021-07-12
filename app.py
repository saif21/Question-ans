from flask import Flask, render_template, url_for, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from sql import InsertData, Question
import os


insert = InsertData()
q = Question()


def get_user():
    user_data = None
    if 'user' in session:
        user = session['user']
        user_data = insert.login(user)
    return user_data


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def index():
    # user = None
    # if 'user' in session:
    #     user = session['user']
    user = get_user()
    answers = q.answers()
    return render_template('home.html', user=user, answers=answers)


@app.route('/register', methods=['POST', 'GET'])
def register():
    user = get_user()
    if request.method == 'POST':
        name = request.form['name']
        passd = request.form['password']
        existing_id = insert.getUserId(name)
        if existing_id:
            err = "User already exists!"
            return render_template('register.html', error=err)
        hash_passd = generate_password_hash(passd, method='sha256')
        insert.insertData(name, hash_passd, '0', '0')
        session['user'] = name
        return redirect(url_for('index'))
    return render_template('register.html', user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    user = get_user()
    error = None
    if request.method == 'POST':
        name = request.form['name']
        passd = request.form['password']
        result = insert.login(name)
        if result:
            if check_password_hash(result['password'], passd):
                session['user'] = result['name']
                return redirect(url_for('index'))
            else:
                error = "Username or Password incorrect!"
        else:
            error = "Username or Password incorrect!"
    return render_template('login.html', user=user, error=error)


@app.route('/logout', methods=['POST', 'GET'])
def logout():

    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def question(question_id):
    user = get_user()
    ques = q.question(question_id)

    return render_template('question.html', user=user, question=ques)


@app.route('/answer/<question_id>', methods=['POST', 'GET'])
def answer(question_id):
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    if user['expert'] == 0:
        return redirect(url_for('index'))
    if request.method == "POST":
        ans = request.form['answer']
        q.submitAns(ans, question_id)
        return redirect(url_for('unanswered'))
    ques = q.singleQuestion(question_id)
    return render_template('answer.html', user=user, question=ques)


@app.route('/ask', methods=['POST', 'GET'])
def ask():
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        ques = request.form['question']
        expert = request.form['expert']
        asked_by_id = user['id']
        q.quesSubmit(ques, asked_by_id, expert)
        return redirect(url_for('index'))
    expert_user = insert.getExpert()
    return render_template('ask.html', user=user, experts=expert_user)


@app.route('/unanswered')
def unanswered():
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    if user['expert'] == 0:
        return redirect(url_for('index'))
    questions = q.allQuestions(user['id'])
    return render_template('unanswered.html', user=user, questions=questions)


@app.route('/users')
def users():
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    if user['admin'] == 0:
        return redirect(url_for('index'))
    user_result = insert.getUsers()
    return render_template('users.html', user=user, users=user_result)


@app.route('/promote/<user_id>')
def promote(user_id):
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    if user['admin'] == 0:
        return redirect(url_for('index'))
    insert.makeExpert(user_id)
    return redirect(url_for('users'))


if __name__ == '__main__':
    app.run(debug=True)
