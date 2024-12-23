"""Blogly application."""


from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# connect to the database
@app.route('/')
  # function displays the homepage
def root():
    """show recent list of posts"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/homepage.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404 

@app.route('/users')
# function displays a page with info on all users
def users_index():
    users= User.query.order_by(User.last_name, User.first_name).all() 
    # return render_template('users/index.html', users=users)
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
# function displays a form to add a new user
def users_new_form():
    return render_template('users/new.html')    

@app.route('/users/new', methods=["Post"])
def users_new():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {new_user.full_name} added.")
    return redirect('/users')

@app.route('/users/<int:user_id>')
# function displays info on a single user
def users_show(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
# function displays a form to edit an existing user
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
# function edits an existing user
def users_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    flash(f"User {user.full_name} edited.")
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
# function deletes an existing user
def users_destroy(user_id)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.full_name} deleted.")
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
# function displays a form to add a post for a specific user
def posts_new_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)  
    
    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
# function displays info on a specific post
def posts_show(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
# function displays a form to edit an existing post
def posts_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
# function edits an existing post
def posts_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' edited.")
    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
# function deletes an existing post
def posts_destroy(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title} deleted.")
    return redirect(f"/users/{post.user_id}")

connect_db(app)
with app.app_context():
    db.create_all()
