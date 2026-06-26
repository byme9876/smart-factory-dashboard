from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///factory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class FactoryData(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    temperature = db.Column(db.Integer)

    machine_status = db.Column(db.String(10))

    efficiency = db.Column(db.Integer)

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

# Home Route
@app.route('/')
def home():

    temperature = random.randint(25, 45)

    machine_status = random.choice(["ON", "OFF"])

    efficiency = random.randint(70, 100)

    # Save data to database
    new_data = FactoryData(
        temperature=temperature,
        machine_status=machine_status,
        efficiency=efficiency
    )

    db.session.add(new_data)

    db.session.commit()

    print("Data inserted successfully")

    # Get latest 5 records for graph
    history = FactoryData.query.order_by(
        FactoryData.id.desc()
    ).limit(5).all()

    history = history[::-1]

    temp_values = [item.temperature for item in history]

    labels = [str(item.id) for item in history]

    return render_template(
        'index.html',
        temperature=temperature,
        machine_status=machine_status,
        efficiency=efficiency,
        temp_values=temp_values,
        labels=labels
    )

# History Route
@app.route('/history')
def history():

    all_data = FactoryData.query.order_by(
        FactoryData.id.desc()
    ).all()

    

    return render_template(
        'history.html',
        records=all_data
    )

# API Route
@app.route('/api/data')
def api_data():

    latest = FactoryData.query.order_by(
        FactoryData.id.desc()
    ).first()

    return {
        "temperature": latest.temperature,
        "machine_status": latest.machine_status,
        "efficiency": latest.efficiency
    }

# Main
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)