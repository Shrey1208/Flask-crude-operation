from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employee_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(255))
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    position = db.Column(db.String(255))

@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html') 
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        Employee_De = Employee_Details(employee_id=employee_id, name=name, age=age, position = position)
        db.session.add(Employee_De)
        db.session.commit()        
        return redirect('/data')

@app.route('/data')
def RetrieveDataList():
    employees = Employee_Details.query.all()
    return render_template('datalist.html',employees = employees)

@app.route('/data/<int:id>')
def RetrieveSingleEmployee(id):
    employee = Employee_Details.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee = employee)
    return f"Employee with id ={id} Doenst exist"

@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    employee = Employee_Details.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = Employee_Details(employee_id=id, name=name, age=age, position = position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does nit exist" 
    return render_template('update.html', employee = employee)

@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    employee = Employee_Details.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/data')
        abort(404)        
    return render_template('delete.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)