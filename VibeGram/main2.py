from flask import Flask, render_template, redirect, url_for, request, flash, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os
from werkzeug.utils import secure_filename
import random
from datetime import datetime, timedelta
import json
import asyncio
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['UPLOAD_FOLDER'] = 'static\profile_pictures'
app.config['STORIES_FOLDER'] = 'static\stories'
app.config['POSTS'] = 'static\posts'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
socketio = SocketIO(app, cors_allowed_origins='*')
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
user_to_show = ""

def move_key_to_front(dct, key):
    if key not in dct:
        return dct

    new_dct = {key: dct[key]}
    for k, v in dct.items():
        if k != key:
            new_dct[k] = v
    return new_dct


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


@app.route('/', methods=['GET', 'POST'])
def redir():
    if request.method == 'GET':
        # username = request.form['username']
        # password = request.form['password']
        # user = User.query.filter_by(username=username).first()

        # if user and check_password_hash(user.password, password):
        #     login_user(user)
        #     # flash('Login successful.', category='success')
        #     return redirect(url_for('home'))
        # else:
        #     flash('Invalid username or password', category='error')
    # if request.method == 'GET':
    #     flash('You have logged out successfully', category='error')   
    # return render_template('login.html')    
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            # flash('Login successful.', category='success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', category='error')
    # if request.method == 'GET':
    #     flash('You have logged out successfully', category='error')   
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
            posts_images.append(line)
    random.shuffle(posts_images)
    cursor.execute(f"SELECT image_name FROM profile_pictures WHERE username = '{current_user.username}'")
    profile_picture = cursor.fetchall()
    if len(profile_picture) > 0:
        for line in profile_picture:
            profile_picture = line[0]
    else:
        profile_picture = "default-no-profile-pic.jpg"
    now = datetime.now()    
    one_day_ago = now - timedelta(days=1)
    formatted_one_day_ago = one_day_ago.strftime("%d/%m/%y %H:%M")
    print(formatted_one_day_ago)
    ### check if user posted in the last 24 hours ###
    cursor.execute(f'select following.is_following, MAX(stories.image_name) as storie_image_name, MAX(profile_pictures.image_name) as profile_picture \
    from stories inner join following on following.is_following = stories.username inner join profile_pictures on profile_pictures.username = \
    stories.username where following.username = "{current_user.username}" and stories.date > "{formatted_one_day_ago}" group by following.is_following order by date DESC')
    results = cursor.fetchall()
    stories = []
    print(posts_images)
    if len(results) > 0:
        for storie in results:
            if storie[0] != current_user.username:
                stories.append(storie)   
    return render_template('home.html', user_does_not_exist=False, posts_images=posts_images, profile_picture=profile_picture, stories=stories)

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
        if int(posts) == 1:
            posts = str(posts)
            posts += " Post"
        else:
            posts = str(posts)
            posts += " Posts"
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
    ## check_followers_count
    cursor.execute(f"SELECT count(*) from following where is_following = '{username}'")
    followers = cursor.fetchall()
    if len(followers) != 0:
        for line in followers:
            followers=line[0]
        if int(followers) == 1:
            followers = str(followers)
            followers += " Follower"
        else:
            followers = str(followers)
            followers += " Followers"     
    else:
        followers="0 followers"
    ## check_following_count
    cursor.execute(f"SELECT count(*) from following where username = '{username}'")
    following = cursor.fetchall()
    if len(following) != 0:
        for line in following:
            following=line[0]
        following = str(following)    
        following += " Following"     
    else:
        following = str(following)
        following="0 following"
    ## get bio
    cursor.execute(f"SELECT bio from profile_bio where username = '{username}'")
    bio = cursor.fetchall()
    if len(bio) > 0:
        for line in bio:
            bio = line[0]
    else:
        bio = "Hi, I'm a VibeGram user! Welcome to my profile."
    return render_template('profile.html', username=username, image=image, posts_images=posts_images, user=username, posts=posts, followers=followers, following=following, bio=bio)


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
    ## check posts_count
    cursor.execute(f"SELECT count(*) from posts where username = '{username}'")
    posts = cursor.fetchall()
    if len(posts) != 0:
        for line in posts:
            posts=line[0]
        if int(posts) == 1:
            posts = str(posts)
            posts += " Post"
        else:
            posts = str(posts)
            posts += " Posts"   
    else:
        posts="0 posts"    
    ## check_followers_count
    cursor.execute(f"SELECT count(*) from following where is_following = '{username}'")
    followers = cursor.fetchall()
    if len(followers) != 0:
        for line in followers:
            followers=line[0]
        if int(followers) == 1:
            followers = str(followers)
            followers += " Follower"
        else:
            followers = str(followers)
            followers += " Followers"     
    else:
        followers="0 followers"
    ## check_following_count
    cursor.execute(f"SELECT count(*) from following where username = '{username}'")
    following = cursor.fetchall()
    if len(following) != 0:
        for line in following:
            following=line[0]
        following = str(following)    
        following += " Following"     
    else:
        following = str(following)
        following="0 following"
    ## get bio
    cursor.execute(f"SELECT bio from profile_bio where username = '{username}'")
    bio = cursor.fetchall()
    if len(bio) > 0:
        for line in bio:
            bio = line[0]
    else:
        bio = "Hi, I'm a VibeGram user! Welcome to my profile."    
    return render_template('search_profile.html', username=username, image=image, posts_images=posts_images, follow_button=follow_button, following=following, followers=followers, posts=posts, bio=bio)


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
    ## check posts_count
    cursor.execute(f"SELECT count(*) from posts where username = '{username}'")
    posts = cursor.fetchall()
    if len(posts) != 0:
        for line in posts:
            posts=line[0]
        if int(posts) == 1:
            posts = str(posts)
            posts += " Post"
        else:
            posts = str(posts)
            posts += " Posts"   
    else:
        posts="0 posts"    
    ## check_followers_count
    cursor.execute(f"SELECT count(*) from following where is_following = '{username}'")
    followers = cursor.fetchall()
    if len(followers) != 0:
        for line in followers:
            followers=line[0]
        if int(followers) == 1:
            followers = str(followers)
            followers += " Follower"
        else:
            followers = str(followers)
            followers += " Followers"     
    else:
        followers="0 followers"
    ## check_following_count
    cursor.execute(f"SELECT count(*) from following where username = '{username}'")
    following = cursor.fetchall()
    if len(following) != 0:
        for line in following:
            following=line[0]
        following = str(following)    
        following += " Following"     
    else:
        following = str(following)
        following="0 following"          
    ## get bio
    cursor.execute(f"SELECT bio from profile_bio where username = '{username}'")
    bio = cursor.fetchall()
    if len(bio) > 0:
        for line in bio:
            bio = line[0]
    else:
        bio = "Hi, I'm a VibeGram user! Welcome to my profile."          
    return render_template('search_profile.html', username=username, image=image, posts_images=posts_images, follow_button=follow_button, posts=posts, followers=followers, following=following, bio=bio)


### GET stories
@app.route('/stories/<string:start_with>', methods=['GET', 'POST'])
@login_required
def view_stories(start_with):
    start_with = start_with.replace("start_with=","")
    images_per_user = {}
    if request.method == "GET":
        username = current_user.username
        now = datetime.now()    
        one_day_ago = now - timedelta(days=1)
        formatted_one_day_ago = one_day_ago.strftime("%d/%m/%y %H:%M")
        query_stories = f"SELECT following.is_following,stories.image_name as storie_image_name, stories.date, profile_pictures.image_name as profile_picture_image_name from following inner \
        join stories on following.is_following = stories.username inner join profile_pictures on stories.username = profile_pictures.username where following.username = '{username}' and date > '{formatted_one_day_ago}'"
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        cursor.execute(query_stories)
        results = cursor.fetchall()
        for line in results:
            user_id = line[0]
            image_id = line[1]
            profile_picture = line[3]

             # if the user ID is already in the dictionary, add the new image ID to the existing list
            if user_id in images_per_user:
                images_per_user[user_id]['images'].append({'image_id': image_id})
            # otherwise, create a new list with the image ID as the first element
            else:
                images_per_user[user_id] = {'profile_picture': profile_picture, 'images': [{'image_id': image_id}]}
        images_per_user = move_key_to_front(images_per_user, start_with)
        for key,value in images_per_user.items():
            print(key,value)
        return render_template('stories.html', images_per_user=images_per_user)

# ### GET stories
# @app.route('/stories/<string:start_with>', methods=['GET', 'POST'])
# @login_required
# def view_stories(start_with):
#     images_per_user = {}
#     if request.method == "GET":
#         username = current_user.username
#         now = datetime.now()    
#         one_day_ago = now - timedelta(days=1)
#         formatted_one_day_ago = one_day_ago.strftime("%d/%m/%y %H:%M")
#         query_stories = f"SELECT following.is_following,stories.image_name as storie_image_name, stories.date, profile_pictures.image_name as profile_picture_image_name from following inner \
#         join stories on following.is_following = stories.username inner join profile_pictures on stories.username = profile_pictures.username where following.username = '{username}' and date > '{formatted_one_day_ago}'"
#         conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
#         cursor = conn.cursor()
#         cursor.execute(query_stories)
#         results = cursor.fetchall()
#         for line in results:
#             user_id = line[0]
#             image_id = line[1]
#             profile_picture = line[3]

#              # if the user ID is already in the dictionary, add the new image ID to the existing list
#             if user_id in images_per_user:
#                 images_per_user[user_id]['images'].append({'image_id': image_id})
#             # otherwise, create a new list with the image ID as the first element
#             else:
#                 images_per_user[user_id] = {'profile_picture': profile_picture, 'images': [{'image_id': image_id}]}

#         # convert the `images_per_user` dictionary to JSON format for use in the template
#         images_json = json.dumps(images_per_user)

#         # render the template with the `images_per_user` dictionary
#         return render_template('stories.html', images=images_json)


### view photo
@app.route('/view_photo/<string:username_image_name>', methods=['GET', 'POST'])
@login_required
def view_photo(username_image_name):
    print("in view_photo")
    if request.method == 'GET' or request.method == "POST":
        username_image_name = username_image_name.replace("username_image_name=", "").split(",")
        print(username_image_name)
        print(len(username_image_name))
        username = username_image_name[0]
        image_name = username_image_name[1]
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT profile_pictures.username, profile_pictures.image_name as profile_picture, posts.image_name as post_image_name from posts inner \
        join profile_pictures on posts.username = profile_pictures.username where posts.username='{username}' and posts.image_name='{image_name}'")
        print(f"SELECT profile_pictures.username, profile_pictures.image_name as profile_picture, posts.image_name as post_image_name from posts inner \
        join profile_pictures on posts.username = profile_pictures.username where posts.username='{username}' and posts.image_name='{image_name}'")
        results = cursor.fetchall()
        comments = ["pretty man","nice photo"]
        if len(results) < 0:
            flash("nothing was found")         
        comments_query = f"select comments.username, comments.image_name, comments.comment_by, comments.comment, profile_pictures.image_name as comment_by_profile_picture \
        from comments INNER JOIN profile_pictures on profile_pictures.username = comments.comment_by where comments.username = '{username}' and comments.image_name = '{image_name}'"
        cursor.execute(comments_query)
        comments_results = cursor.fetchall()
        if len(comments_results) > 0:
            print(comments_results)
        if username == current_user.username:
            return render_template('edit_post.html', results=results, comments=comments_results)
        else:    
            return render_template('view_photos.html', results=results, comments=comments_results)


### view photo
@app.route('/edit_post/<string:username_image_name>', methods=['GET', 'POST'])
@login_required
def edit_post(username_image_name):
    print("in view_photo")
    if request.method == 'GET' or request.method == "POST":
        username_image_name = username_image_name.replace("username_image_name=", "").split(",")
        print(username_image_name)
        print(len(username_image_name))
        username = username_image_name[0]
        image_name = username_image_name[1]
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT profile_pictures.username, profile_pictures.image_name as profile_picture, posts.image_name as post_image_name from posts inner \
        join profile_pictures on posts.username = profile_pictures.username where posts.username='{username}' and posts.image_name='{image_name}'")
        print(f"SELECT profile_pictures.username, profile_pictures.image_name as profile_picture, posts.image_name as post_image_name from posts inner \
        join profile_pictures on posts.username = profile_pictures.username where posts.username='{username}' and posts.image_name='{image_name}'")
        results = cursor.fetchall()
        comments = ["pretty man","nice photo"]
        if len(results) < 0:
            flash("nothing was found")         
        comments_query = f"select comments.username, comments.image_name, comments.comment_by, comments.comment, profile_pictures.image_name as comment_by_profile_picture \
        from comments INNER JOIN profile_pictures on profile_pictures.username = comments.comment_by where comments.username = '{username}' and comments.image_name = '{image_name}'"
        cursor.execute(comments_query)
        comments_results = cursor.fetchall()
        if len(comments_results) > 0:
            print(comments_results)

        return render_template('edit_post.html', results=results, comments=comments_results)


### add comment
@app.route('/delete_post/<string:username_image_name>', methods=['GET', 'POST'])
@login_required
def delete_post(username_image_name):
    if request.method == "GET" or request.method == "POST":
        # time.sleep(1)
        # username = current_user.username
        username_image_name = username_image_name.replace("username_image_name=","").split(",")
        if username_image_name[0] == current_user.username:
            conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM POSTS WHERE username='{username_image_name[0]}' and image_name='{username_image_name[1]}'")
            conn.commit()
            cursor.execute(f"DELETE FROM comments WHERE username='{username_image_name[0]}' and image_name='{username_image_name[1]}'")
            conn.commit()
            return redirect(url_for('profile'))
        else:
            return("Not Authorized")  
        # conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        # cursor = conn.cursor()
        # cursor.execute(f'insert into comments (username,image_name, comment_by, comment) \
        # VALUES ( "{comment[0]}", "{comment[1]}", "{username}","{comment[2]}")')
        # conn.commit()
        # return redirect(url_for('view_photo', username_image_name=f"{comment[0]},{comment[1]}"))


### add comment
@app.route('/add_comment/<string:comment>', methods=['GET', 'POST'])
@login_required
def add_comment(comment):
    if request.method == "GET" or request.method == "POST":
        # time.sleep(1)
        username = current_user.username
        comment = comment.replace("comment=","").split("`")
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        cursor.execute(f'insert into comments (username,image_name, comment_by, comment) \
        VALUES ( "{comment[0]}", "{comment[1]}", "{username}","{comment[2]}")')
        conn.commit()
        return redirect(url_for('view_photo', username_image_name=f"{comment[0]},{comment[1]}"))        


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
@app.route('/change_bio/<string:bio>', methods=['GET', 'POST'])
@login_required
def change_bio(bio):
    bio = str(bio)
    print(bio)
    if request.method == "POST" or request.method == "GET":
        username = current_user.username
        # bio = bio[4:]
        # profile_username = request.args.get('profile_username')
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM bio where username = '{username}'")
            conn.commit()
        except:
            print("no records")
        bio = str(bio).replace('"', "'")    
        cursor.execute(f'INSERT INTO profile_bio values ("{username}","{bio}")')
        conn.commit()
        # global user_to_show
        # user_to_show = profile_username
        # return(f"You: {username} will follow {profile_username}")
        return redirect(url_for('profile'))


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

# Add a new route to handle the image upload story
@app.route('/add-story', methods=['POST'])
@login_required
def add_story():
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
        # try:
        #     cursor.execute(f"DELETE FROM stories where username = '{username}'")
        #     conn.commit()
        # except:
        #     print("issue with deleting")
        now = datetime.now()
        formatted_now = now.strftime("%d/%m/%y %H:%M")
        cursor.execute(f"insert into stories values('{username}','{filename}', '{formatted_now}')")
        # print(f"update profile_pictures set username = '{username}' image_name='{filename}' where username = '{username}'")
        conn.commit()
        file.save(os.path.join(app.config['STORIES_FOLDER'], filename))
        return redirect(url_for('home'))
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

# @app.route('/direct_messages')
# def direct_messages():
#     return render_template('direct_messages.html')


# @socketio.on('message')
# def handle_message(message):
#     print('Message: ' + message)
#     emit('message', message, broadcast=True)

@app.route('/chat/<user1_id>/<user2_id>')
@login_required
def chat(user1_id, user2_id):
    if current_user.username == user1_id or current_user.username == user2_id:
        room_id = sorted([user1_id, user2_id], key=str)
        room_id = f"{room_id[0]}-{room_id[1]}"
        print(current_user.username)
        print(user1_id)
        print(user2_id)
        #### get previous chat 
        conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT sender, message, date, image_name as profile_picture FROM direct_messages\
        INNER JOIN profile_pictures ON profile_pictures.username = direct_messages.sender WHERE (sender = '{user1_id}' OR b_party = '{user1_id}') \
        AND (sender = '{user2_id}' OR b_party = '{user2_id}') ORDER BY date")
        print(f"SELECT sender, message, date, image_name as profile_picture FROM direct_messages\
        INNER JOIN profile_pictures ON profile_pictures.username = direct_messages.sender WHERE sender = '{user1_id}' OR b_party = '{user1_id}' \
        AND sender = '{user2_id}' OR b_party = '{user2_id}' ORDER BY date")
        results = cursor.fetchall()
        if len(results) > 0:
            for message in results:
                print(message)
        else:
            print("No existing messages")
        return render_template('direct_messages.html', room=room_id, previous_messages=results, username=current_user.username)
  
    else:     
        return("Unauthorized")     


@socketio.on('message')
def handle_message(message, room, sender):
    ## get_profile_picture
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT image_name from profile_pictures where username='{current_user.username}'")
    result = cursor.fetchall()
    image_name = ("default-no-profile-pic.jpg")
    if len(result) >= 0:
        for line in result:
            image_name = line[0]
        print(image_name)  
    #### get date and time ####
    now = datetime.now() 
    now = now.strftime("%d/%m/%y %H:%M")
    #####
    ##### insert message into database
    usernames = room.split("-")
    if usernames[0] == current_user.username:
        b_party = usernames[1]
    elif usernames[1] == current_user.username:   
        b_party = usernames[0]
    query = f'INSERT INTO direct_messages (sender, b_party, message, date)\
    VALUES("{current_user.username}", "{b_party}", "{message}", "{now}")'
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\VibeGram\database\database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print(room)
    print(f'Room {room}: {sender}: {message}')
    emit('message', {'text': message, 'sender': current_user.username, 'profile_picture': image_name, 'datetime': now}, room=room) 


@socketio.on('join')
def on_join(room):
    join_room(room)
    # emit('message', 'User has joined the room.', room=room)

@socketio.on('leave')
def on_leave(room):
    leave_room(room)
    # emit('message', 'User has left the room.', room=room)     


if __name__ == '__main__':
    app.run(debug=True)