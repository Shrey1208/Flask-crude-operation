from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'  # Replace with your database URL
db = SQLAlchemy(app)

# Define the database model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    description = request.form['description']
    new_item = Item(name=name, description=description)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

@app.route('/delete_item/<int:id>')
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

