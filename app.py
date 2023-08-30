from flask import (
    Flask,
    render_template,
    session,
    request,
    render_template,
    redirect,
    make_response,
    flash,
)

from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


users = {}  # Placeholder to store registered

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

#########################################################################
# Login routes

@app.route("/")
def index():
    return render_template(
        "home.html",
        title="Blogly Bytes: Bites of Insight and Inspiration",
        Description="Smarter page templates with Flask & Jinja",
    )


@app.route("/flask-info")
def flask_info():
    return render_template("flask-info.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if username in users:
            flash("Username already exists!")
        elif password != confirm_password:
            flash("Passwords do not match!")
        else:
            # Store the user details in a dictionary or database
            users[username] = password
            flash("Registration successful! Please log in.")
            return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Perform login process
        username = request.form["username"]
        password = request.form["password"]

        # Validate user credentials
        if username in users and users[username] == password:
            # Set session variables or user tokens for authentication
            session["logged_in"] = True
            session["username"] = username
            flash("Login successful!")
            return render_template(
                "flask-info.html",
            )
        else:
            flash("Invalid username or password!")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


#########################################################################
# User routes

@app.route('/users')
def users_index():
    """Show a page with info on all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""

    return render_template('users/new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/users")
  
  
if __name__ == '__main__':
    app.run(debug=True)