from flask import Flask, render_template, request, redirect, url_for, flash, session
import os, uuid, datetime, time

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())

def log(err):
    with open('log.txt', 'a') as f:
        f.write(f'[{datetime.datetime.now()}] {err}')
        f.write('\n')

def create_link(data):
    try:
        id_ = str(uuid.uuid4())
        f = open(f'templates/{id_}.html', 'w')
        f.write(data)
        f.close()
        return f'http://{request.remote_addr}:5000/{id_}'
    except Exception as e:
        log(e)
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['link']
        link = create_link(data)
        if link:
            return render_template('index.html', link=link)
        else:
            flash('Error creating link!')
            return render_template('index.html')
    else:
        return render_template('index.html', link='')

@app.route('/<id>')
def link(id):
    filename = f'{id}.html'
    if os.path.isfile(f'templates/{filename}'):
        try:
            if session['visited'] == True:
                os.remove(f'templates/{filename}')
                session.clear()
                return redirect(url_for('index'))
        except(KeyError):
            session['visited'] = True
            return render_template(filename)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)