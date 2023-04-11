from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Initialize PyMongo
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        duedate = request.form['duedate']  # retrieve due date from form data
        todos.insert_one({'content': content, 'degree': degree, 'duedate': duedate})  # add due date to MongoDB document
        return redirect(url_for('index'))

    all_todos = todos.find().sort([('duedate', 1)])  # sort todos by due date (ascending order)
    return render_template('index.html', todos=all_todos)


@app.route('/<id>/delete/', methods=['POST'])
def delete(id):
    todos.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))


@app.route('/<id>/edit/', methods=('GET', 'POST'))
def edit(id):
    todo = todos.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.update_one({'_id': ObjectId(id)}, {'$set': {'content': content, 'degree': degree}})
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo)


@app.route('/<id>/update/', methods=('GET', 'POST'))
def update(id):
    todo = todos.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        duedate = request.form['duedate']
        todos.update_one({'_id': ObjectId(id)}, {'$set': {'content': content, 'degree': degree, 'duedate': duedate}})
        return redirect(url_for('index'))

    return render_template('update.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)
