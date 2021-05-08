from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Database and DB Initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_practice_development'
db = SQLAlchemy(app)

# User model definition


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

# Entry model definition


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Entry %r>' % self.id

# Index for all entries & POST to create an Entry


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        entry_content = request.form['content']
        new_entry = Entry(content=entry_content)
        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an error creating your entry'

    else:
        entries = Entry.query.order_by(Entry.created_at).all()
        return render_template('index.html', entries=entries)

# Destroy an entry


@app.route('/delete/<int:id>')
def delete(id):
    entry_to_delete = Entry.query.get_or_404(id)

    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an error deleting that entry'


if __name__ == "__main__":
    app.run(debug=True)
