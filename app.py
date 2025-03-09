from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from ai_writer import generate_blog_post
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)

with app.app_context():
    db.create_all()

# Function to auto-generate and save a post
def auto_generate_and_save_post():
    topic = "How to build wealth using AI and automation"
    content = generate_blog_post(topic)
    post = BlogPost(title=topic, content=content)
    db.session.add(post)
    db.session.commit()
    print("✅ Auto-generated blog post created and saved.")

# Homepage route
@app.route('/')
def home():
    posts = BlogPost.query.order_by(BlogPost.id.desc()).all()
    return render_template("index.html", posts=posts)

# Manual trigger route
@app.route('/generate')
def generate():
    auto_generate_and_save_post()
    return "A new AI-generated post was successfully created and saved!"

if __name__ == '__main__':
    # Scheduler initialization directly in main block
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=auto_generate_and_save_post, trigger="interval", hours=24)
    scheduler.start()

    app.run(debug=True)
