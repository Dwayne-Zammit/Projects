from flask import Flask , request , abort , redirect , Response ,url_for, render_template
from flask_login import LoginManager , login_required , UserMixin , login_user, current_user
from flask import Flask, jsonify
from flask import Flask, jsonify
import boto3
from flask import Flask, jsonify
import boto3
import boto3
import os
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
import time
from flask import send_file

output_directory = 'rdp_files'
username = "Administrator"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
region = "eu-west-1"

class User(UserMixin):
    def __init__(self , username , password , id , active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return make_secure_token(self.username , key='secret_key')

class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def get_user(self, username):
        return self.users.get(username)

    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)

    def next_index(self):
        self.identifier +=1
        return self.identifier

users_repository = UsersRepository()

@app.route('/')
# @login_required
def index():
    return redirect(url_for('home'))
    # return f"Hello {current_user.username} welcome to the learning portal"

@app.route('/home')
# @login_required
def home():
    return render_template("home.html")
    # return f"Hello {current_user.username} welcome to the learning portal"
    

@app.route('/launch_lab')
# @login_required
def launch_lab():
    if request.method == "GET":
        return render_template("launch_lab.html")
    else:
        return "post"  

@app.route('/login' , methods=['GET' , 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        print("in post")
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        registereduser = users_repository.get_user(username)
        print('Users '+ str(users_repository.users))
        # print('Register user %s , password %s' % (registereduser.username, registereduser.password))
        if registereduser != None and registereduser.password == password:
            print('Logged in..')
            login_user(registereduser)
            return redirect(url_for('home'))
        else:
            return abort(401)


@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        new_user = User(username , password , users_repository.next_index())
        users_repository.save_user(new_user)
        return Response("Registered Successfully")

#handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

#callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return users_repository.get_user_by_id(userid)


# @app.route('/instance_password/<string:instance_id>', methods=['GET'])
def get_password(instance_id):
        # Get password data
        ec2_client = boto3.client('ec2',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region)
        response = ec2_client.get_password_data(
            InstanceId=instance_id,
            DryRun=False
        )
        ciphertext = response['PasswordData']
        key_path = 'aws_key\LaunchWindows.pem'
        with open(key_path, 'r') as privkeyfile:
            key_text = privkeyfile.read()
        print(f"key text is {key_text}")
        ciphertext = ''
        while ciphertext == '':
            print("attempting to get passsword")
            response = ec2_client.get_password_data(
                InstanceId=instance_id,
                DryRun=False
            )
            ciphertext = response['PasswordData']
            try:
                rdp_pw = decrypt(key_text, ciphertext)
            except:
                print("error decrypting")
                time.sleep(1)
        print(rdp_pw)
        return rdp_pw

def decrypt(key_text, password_data):
    key = RSA.importKey(key_text)
    cipher = PKCS1_v1_5.new(key)
    decrypted_data = cipher.decrypt(base64.b64decode(password_data), None)
    return decrypted_data.decode('utf-8')


@app.route('/launch_instance', methods=['GET'])
def launch_instance():
    if request.method == "GET":
        ### uncomment this to mock a test to not wait ##
        # return jsonify(
        #     password='helloguhigigiugiugigigigolpq', 
        #     filepath='hellopath', 
        #     public_ip='ip1234567'
        # )
        print("launching instance")
        # Create an EC2 client
        ec2_client = boto3.client('ec2',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region)

        # Specify the ID of your launch template
        launch_template_id = os.getenv("WINDOWS_LAUNCH_TEMPLATE_ID")

        # Launch the EC2 instance using the launch template
        response = ec2_client.run_instances(
            LaunchTemplate={
                'LaunchTemplateId': launch_template_id
            },
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        print(instance_id)
        # time.sleep(130)
        # Retrieve the instance details
        instance = ec2_client.describe_instances(InstanceIds=[instance_id])
        public_ip = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
        print(instance_id)
        print(public_ip)
        rdp_pw = ''
        rdp_pw =  get_password(instance_id)
        public_ip = get_instance_public_ip(instance_id)
        print(public_ip)
        rdp_filepath = generate_rdp_file(public_ip)
        print(f"RDP file generated for IP {public_ip}: {rdp_filepath}")
        return jsonify(
            password=rdp_pw, 
            filepath=rdp_filepath, 
            public_ip=public_ip
        )

def get_instance_public_ip(instance_id):
    # Create an EC2 client
    ec2_client = boto3.client('ec2',
                              region_name=region,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

    # Retrieve information about the instance
    response = ec2_client.describe_instances(InstanceIds=[instance_id])

    # Check if the instance exists
    if 'Reservations' in response and response['Reservations']:
        instances = response['Reservations'][0]['Instances']
        if instances:
            instance = instances[0]
            if 'PublicIpAddress' in instance:
                public_ip = instance['PublicIpAddress']
                public_ip.replace(".","_")
                return public_ip
   

def generate_rdp_file(ip_address):
    template = """\
full address:s:{ip_address}
username:s:{username}
"""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    rdp_content = template.format(ip_address=ip_address, username=username)
    rdp_filename = f"{ip_address}_rdp.rdp"
    rdp_filepath = os.path.join(output_directory, rdp_filename)
    print(rdp_filepath)
    print(rdp_filename)
    with open(rdp_filepath, "w") as rdp_file:
        rdp_file.write(rdp_content)

    return rdp_filename


@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    print(filename)
    file_path = f'rdp_files\{filename}'
    print(file_path)
    # Check if the file exists
    if os.path.isfile(file_path):
        # Return the file as a download response
        return send_file(file_path)
    else:
        return 'File not found'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)