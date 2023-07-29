from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['UPLOAD_FOLDER'] = 'static\profile_pictures'
app.config['POSTS'] = 'static\posts'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
user_to_show = ""


def get_profile_picture(username):
    ## sqlite db connection
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
    cursor = conn.cursor()
    cursor.execute(f"select image_name from profile_pictures where username = '{username}'")
    result = cursor.fetchall()
    conn.close()
    for profile_picture in result:
        return profile_picture[0]

# Create a function to check if the uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.before_first_request
def create_tables():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful.', category='success')
            return redirect(url_for('home'))

        flash('Invalid username or password', category='error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Both username and password are required.', category='error')
            return render_template('register.html')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', category='error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', category='success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
    cursor = conn.cursor()
    cursor.execute(f"select posts.username, posts.image_name, profile_pictures.image_name as profile_picture from following \
    inner join posts on posts.username = is_following inner join profile_pictures on profile_pictures.username = following.is_following where following.username = '{current_user.username}'")
    results = cursor.fetchall()
    posts_images = []
    if len(results) != 0:
        for line in results:
            print(line)
            posts_images.append(line)
    print(posts_images)
    return render_template('home.html', user_does_not_exist=False, posts_images=posts_images)

@app.route('/profile')
@login_required
def profile():
    username = current_user.username
    image = get_profile_picture(username)
    if str(image) == "None":
        print("no profile picture yet")
        image = "default-no-profile-pic.jpg"
    image_path = r"static\profile_pictures"
    image = image_path + "\\" + image
    # try to get posts
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT image_name from posts where username = '{username}'")
    results = cursor.fetchall()
    cursor.execute(f"SELECT count(image_name) from posts where username = '{username}'")
    posts = cursor.fetchall()
    if len(posts) != 0:
        for post in posts:
            posts = post[0]
    else:
        posts = 0  
    posts_images = []
    # post_images_html = []
    if len(results) != 0:
        for result in results:
            for image_name in result:
                posts_images.append(image_name)
    print(posts_images)
    # for i in posts_images:
    #     post_images_html.append(f'<img class="grid-item" src="static/image/{i}" alt="{i}">')
    # print(post_images_html)
    return render_template('profile.html', username=username, image=image, posts_images=posts_images, user=username, posts=posts)


@app.route('/search_profile', methods=['GET', 'POST'])
@login_required
def search_profile():
    # if request.method == "POST" or request.method == "GET":
    follow_button = "True"
        # print("args below")
        # print(args)
    if request.method == "GET":
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        # try:
        #     last_followed = cursor.execute(f"SELECT * from following where username = '{current_user.username}'")
        #     for i in last_followed:
        #         print(i)
        #         username = i[1]
        #     print("in get")
        # except:
        username = user_to_show
    elif request.method == "POST":
        print("in post")
        username = request.form.get('search_username')
    print("username below")
    # print(username) 

    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\instance\login.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * from user where username = '{username}'")
        result = cursor.fetchall()
    except:
        username = user_to_show
    if username == current_user.username:
        return render_template('home.html', user_does_not_exist="own_user", user=username)
    try:    
        if len(result) == 0:
            print("user does not exist")
            return render_template('home.html', user_does_not_exist=True, user=username)
    except:
        print("we did not do a query")        
    # username = current_user.username
    image = get_profile_picture(username)
    if str(image) == "None":
        print("no profile picture yet")
        image = "default-no-profile-pic.jpg"
    image_path = r"static\profile_pictures"
    image = image_path + "\\" + image
    # try to get posts
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT image_name from posts where username = '{username}'")
    results = cursor.fetchall()
    ## check if already following
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from following where username = '{current_user.username}' and is_following = '{username}'")
    is_following = cursor.fetchall()
    if len(is_following) != 0:
        follow_button = "False"
    print(follow_button)    
    posts_images = []
    # post_images_html = []
    if len(results) != 0:
        for result in results:
            for image_name in result:
                posts_images.append(image_name)
    print(posts_images)
    # for i in posts_images:
    #     post_images_html.append(f'<img class="grid-item" src="static/image/{i}" alt="{i}">')
    # print(post_images_html)
    print("username below")
    print(type(username))
    print(type(image))
    print(type(posts_images))
    print(type(follow_button))
    return render_template('search_profile.html', username=username, image=image, posts_images=posts_images, follow_button=follow_button)


@app.route('/Search_profile', methods=['GET', 'POST'])
@login_required
def Search_profile():
    username=request.args.get('profile_username')
    # if request.method == "POST" or request.method == "GET":
    follow_button = "True"
    print(username)
        # print("args below")
        # print(args)
    # if request.method == "GET":
    #     conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
    #     cursor = conn.cursor()
    #     # try:
    #     #     last_followed = cursor.execute(f"SELECT * from following where username = '{current_user.username}'")
    #     #     for i in last_followed:
    #     #         print(i)
    #     #         username = i[1]
    #     #     print("in get")
    #     # except:
    #     username = user_to_show
    # elif request.method == "POST":
    #     print("in post")
    #     username = request.form.get('search_username')
    print("username below")
    # print(username) 

    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\instance\login.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * from user where username = '{username}'")
        result = cursor.fetchall()
    except:
        username = user_to_show
    if username == current_user.username:
        return render_template('home.html', user_does_not_exist="own_user", user=username)
    try:    
        if len(result) == 0:
            print("user does not exist")
            return render_template('home.html', user_does_not_exist=True, user=username)
    except:
        print("we did not do a query")        
    # username = current_user.username
    image = get_profile_picture(username)
    if str(image) == "None":
        print("no profile picture yet")
        image = "default-no-profile-pic.jpg"
    image_path = r"static\profile_pictures"
    image = image_path + "\\" + image
    # try to get posts
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT image_name from posts where username = '{username}'")
    results = cursor.fetchall()
    ## check if already following
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from following where username = '{current_user.username}' and is_following = '{username}'")
    is_following = cursor.fetchall()
    if len(is_following) != 0:
        follow_button = "False"
    print(follow_button)    
    posts_images = []
    # post_images_html = []
    if len(results) != 0:
        for result in results:
            for image_name in result:
                posts_images.append(image_name)
    print(posts_images)
    # for i in posts_images:
    #     post_images_html.append(f'<img class="grid-item" src="static/image/{i}" alt="{i}">')
    # print(post_images_html)
    print("username below")
    print(type(username))
    print(type(image))
    print(type(posts_images))
    print(type(follow_button))
    return render_template('search_profile.html', username=username, image=image, posts_images=posts_images, follow_button=follow_button)


### follow user
@app.route('/follow_user/<string:profile_username>', methods=['GET', 'POST'])
@login_required
def follow_user(profile_username):
    if request.method == "POST":
        username = current_user.username
        # profile_username = request.args.get('profile_username')
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO following values ('{username}','{profile_username}')")
        conn.commit()
        global user_to_show
        user_to_show = profile_username
        # return(f"You: {username} will follow {profile_username}")
        return redirect(url_for('search_profile'))


### unfollow user
@app.route('/unfollow_user/<string:profile_username>', methods=['GET', 'POST'])
@login_required
def unfollow_user(profile_username):
    if request.method == "POST":
        username = current_user.username
        # profile_username = request.args.get('profile_username')
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        cursor.execute(f"delete from following where username='{username}' and is_following='{profile_username}'")
        conn.commit()
        global user_to_show
        user_to_show = profile_username
        # return(f"You: {username} will follow {profile_username}")
        return redirect(url_for('search_profile'))


# Add a new route to handle the image upload profile picture
@app.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    username = current_user.username
    if 'image' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        flash('Image uploaded successfully', category='success')
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM profile_pictures where username = '{username}'")
            conn.commit()
        except:
            print("issue with deleting")

        cursor.execute(f"insert into profile_pictures values('{username}','{filename}')")
        # print(f"update profile_pictures set username = '{username}' image_name='{filename}' where username = '{username}'")
        conn.commit()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('profile'))
    else:
        flash('Invalid file type', category='error')
        return redirect(request.url)

# Add a new route to handle the image upload post
@app.route('/upload-post', methods=['POST'])
@login_required
def upload_post():
    username = current_user.username
    if 'image' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        flash('Image uploaded successfully', category='success')
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        cursor.execute(f"insert into posts values('{username}','{filename}')")
        # print(f"update profile_pictures set username = '{username}' image_name='{filename}' where username = '{username}'")
        conn.commit()
        file.save(os.path.join(app.config['POSTS'], filename))
        return redirect(url_for('profile'))
    else:
        flash('Invalid file type', category='error')
        return redirect(request.url)

            
if __name__ == '__main__':
    app.run(debug=True)