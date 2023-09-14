from flask import (Flask, render_template,
                   url_for, request,
                   redirect, make_response,
                   )

app = Flask(__name__)
app.secret_key = b'9ae25f7d96c6ca1ba6072c14a461b88f20b6c025a35fc41062dc93638e8bb0bd'


# index
@app.route('/')
@app.route('/index/')
def index():
    context = {
        'title': 'Lesson 2',
        'links_block': [
            {'link_name': 'Задача 7', 'url': url_for('calculate_form')},
            {'link_name': 'Задача 9', 'url': url_for('cookie_user')}
        ]
    }
    return render_template('index.html', **context)


# task 07
@app.route('/calculate_form', methods=('POST', 'GET'))
def calculate_form():
    content = {
        'title': 'Задание 7',
    }
    if request.method == 'POST':
        a_number = request.form.get('number')
        if not a_number:
            return render_template('calculate_form.html')
        a_number = int(a_number)
        return redirect(url_for('calculate_result', num=a_number))
    return render_template('calculate_form.html', **content)


@app.route('/calculate_result/<int:num>')
def calculate_result(num):
    content = {
        'title': 'Задание 7, результат',
        'a_number': num,
        'number_sq': num * num,
    }
    return render_template('calculate_result.html', **content)


# task 09
@app.route('/cookie-user', methods=('GET', 'POST'))
def cookie_user():
    if request.method == 'POST':

        if (not request.form.get('username')
                or not request.form.get('email')):
            return redirect(url_for('cookie_user'))

        content = {
            'title': 'Задание 9, результат',
            'username': request.form['username'],
            'email': request.form['email'],
        }
        response = make_response(
            render_template('task09_response.html', **content)
        )
        response.set_cookie('username', request.form['username'])
        response.set_cookie('email', request.form['email'])
        return response
    return render_template('task09_form.html', title='Задание 9')


@app.route('/cookie-logout')
def cookie_response():
    response = make_response(redirect('cookie-user'))
    response.delete_cookie('username')
    response.delete_cookie('email')
    return response


if __name__ == '__main__':
    app.run(debug=True)