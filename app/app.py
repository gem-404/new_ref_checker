#! /usr/bin/python3

# Import the necessary libraries...
from flask import Flask, render_template, request
from flask import redirect, session, url_for
from flask.helpers import flash
from werkzeug.utils import secure_filename
import docx
import os
import urllib.parse
import re
import mysql.connector
from dotenv import load_dotenv

from hashlib import sha256


load_dotenv()

app = Flask(__name__)

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

UPLOAD_FOLDER = 'docx_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = os.getenv("SECRET_KEY")


db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to MySQL
mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
)


def hash_password(password: str) -> str:
    """
    Hashes passwords using sha256

    """
    password = password.replace(" ", "").replace("\t", "").replace("\n", "")
    password_bytes = password.encode('utf-8')
    hashed_password = sha256(password_bytes)

    return hashed_password.hexdigest()


def check_login(username: str, password: str) -> bool:
    """
    Check if the username and password match a registered user
    """

    cursor = mydb.cursor()

    query = "SELECT * FROM Users WHERE username = %s AND password_hash = %s"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()
    cursor.close()

    if result:
        return True

    return False


def check_signup(email: str) -> bool:
    """
    Check if the email provided is already in the database and return False
    if email is already registered.
    """

    cursor = mydb.cursor()

    query = "SELECT * FROM Users WHERE email = %s"

    cursor.execute(query, (email,))

    result = cursor.fetchone()

    cursor.close()

    if result:
        return False

    return True


def is_logged_in():
    """
    Check if the user is logged in
    """

    return "username" in session


def underline_citations(text):
    new_pattern = r"""
    \( # Opening parenthesis
    (?: # Non-capturing group for the entire citation content
        (?:(\d{4})[,\s]*)? # Optional year at the beginning (for AMA style)
        [\w\s,.&]+? # Author names or citation key(inc. organizations, &, etc.)
        (?:et al\.)? # Optional "et al."
        (?:,?\s*\d{4})? # Optional year (if not at the beginning)
        (?:,?\s*p?p?\.?\s*\d+(?:-\d+)?)? # Optional page numbers
    |
        \d+ # For numeric styles, just a number
        (?:[-,]\d+)* # Optional continuation for ranges or lists
        (?:,\s*p\.?\s*\d+)? # Optional page number for numeric styles
    )
    \) # Closing parenthesis
    """

    regex = re.compile(new_pattern, re.VERBOSE)
    return regex.sub(r"<span class='citation'>\g<0></span>", text)


def read_docx(file_path: str) -> str:
    """
    Reads the contents of the docx file given.
    """

    doc = docx.Document(file_path)

    full_text: list[str] = []

    for para in doc.paragraphs:
        underlined_text = underline_citations(para.text)
        full_text.append(underlined_text)

    return '\n\n'.join(full_text)


# Update the upload route to ensure proper functionality
@app.route('/upload')
def upload():
    """
    Upload view.
    """

    if is_logged_in():
        return render_template('upload.html')
    if not is_logged_in():
        flash("Please log in or sign up to upload a file!", 'warning')
        return redirect(url_for('login'))
    else:
        return render_template('upload.html')


@app.route('/signup')
def signup():
    """
    Signup Page
    """

    return render_template('signup.html')


@app.route('/signing', methods=['POST'])
def new_signup():
    """
    Sign up new users...
    """

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash("Password and Confirm Password do not match!", 'error')
            return redirect(url_for('signup'))

        if email:
            if check_signup(email):
                cursor = mydb.cursor()
                query = """INSERT INTO Users (username, email, password_hash)
                VALUES (%s, %s, %s)"""

                hashed_password = hash_password(password)

                cursor.execute(query, (username, email, hashed_password))
                mydb.commit()
                cursor.close()
                session['username'] = username

                flash("Sign up successful! You are now logged in.", 'success')
                return redirect(url_for('upload'))
            else:
                flash("Email Already Signed Up")

    return redirect(url_for('signup'))


@app.route('/login')
def login():
    """
    login page
    """

    return render_template('login.html')


@app.route('/logging', methods=['POST'])
def do_login():
    """
    Authenticate and log in the user.
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        p_hash = hash_password(password)

        if username and password:
            if check_login(username, p_hash):
                session['username'] = username
                flash("Login successful", 'success')
                return redirect(url_for('upload'))

            else:
                err_msg = "Invalid username or password. Please try again!"
                flash(err_msg, 'error')
                return redirect(url_for('login'))

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """
    Log out the user.
    """

    session.pop('username', None)
    flash("You have been logged out.", 'info')
    return redirect(url_for('login'))


@app.route('/readfile', methods=['POST'])
def readfile():
    if 'myfile' not in request.files:
        return render_template('upload.html')

    myfile = request.files['myfile']

    myfile.filename = str(myfile.filename)
    
    if myfile.filename == '':
        return render_template('upload.html')

    # Save the file to the UPLOAD_FOLDER
    filename = secure_filename(myfile.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    myfile.save(file_path)

    # Pass only the filename or identifier through the URI
    quoted_filename = urllib.parse.quote(filename)
    return redirect(url_for('index', doc_filename=quoted_filename))


@app.route('/')
def index():
    """
    Index view.
    """

    # Check if there is uploaded document content.
    doc_filename = request.args.get('doc_filename', None)

    if not doc_filename:
        # If no uploaded content, use the example docx file
        doc_filename = "selva.docx"

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc_filename)
    doc_content = read_docx(file_path)

    session['doc_filename'] = doc_filename
    return render_template('home.html', doc_content=doc_content)


def main():
    """
    Main function.
    """
    app.run(host='0.0.0.0', port=5500, debug=True)


if __name__ == "__main__":
    main()
