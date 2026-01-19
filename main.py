import os
import pdfkit
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import wikipediaapi

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///textbooks.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Textbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_wikipedia_content(topic):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(topic)
    return (page.text, page.fullurl) if page.exists() else (None, None)

def create_textbook(topics):
    os.makedirs('textbooks', exist_ok=True)
    combined_content = ""
    for topic in topics:
        content, url = get_wikipedia_content(topic.strip())
        if content:
            combined_content += f"# {topic.strip()}\n\n[Read more here]({url})\n\n" + content + "\n\n---\n\n"
        else:
            flash(f"Sorry, the topic '{topic}' does not exist on Wikipedia.")
    return combined_content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topics = request.form['topics'].split(',')
        content = create_textbook(topics)
        if content:
            textbook = Textbook(title=", ".join(topics), content=content, user_id=current_user.id)
            db.session.add(textbook)
            db.session.commit()
            flash("Textbook created successfully!")
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/textbooks')
@login_required
def textbooks():
    user_textbooks = Textbook.query.filter_by(user_id=current_user.id).all()
    return render_template('textbooks.html', textbooks=user_textbooks)

@app.route('/delete_textbook/<int:textbook_id>')
@login_required
def delete_textbook(textbook_id):
    textbook = Textbook.query.get_or_404(textbook_id)
    db.session.delete(textbook)
    db.session.commit()
    flash("Textbook deleted successfully!")
    return redirect(url_for('textbooks'))

@app.route('/export_pdf/<int:textbook_id>')
@login_required
def export_pdf(textbook_id):
    textbook = Textbook.query.get_or_404(textbook_id)
    pdfkit.from_string(textbook.content, f'textbooks/{textbook.title}.pdf')
    flash("PDF exported successfully!")
    return redirect(url_for('textbooks'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        flash("Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
