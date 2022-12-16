from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
from flask import request
import string
import random
import subprocess
import requests as req

app = Flask(__name__)

CORS(app, support_credentials=True)

address = "http://64.227.148.75:5000/"


@app.route("/ssl/save-code",  methods = ['POST'])
@cross_origin(supports_credentials=True)
def save_code_ssl():
    if request.method=="POST":
        request_data = request.get_json()
        code = request_data['code'].strip()
        container_name = request_data['container_name'].strip();
        url = address + "save-code"
        myobj = {"container_name":container_name,"code":code}
        resp = req.post(url, json = myobj)
        return resp.text


@app.route("/ssl/create-new-container")
@cross_origin(supports_credentials=True)
def create_new_container_ssl():
    request_data = request.args
    image_name = request_data['image_name']
    url = address + f"create-new-container?image_name={image_name}"
    resp = req.get(url)
    return resp.text


@app.route("/ssl/delete-container")
@cross_origin(supports_credentials=True)
def delete_container_ssl():
    request_data = request.args
    container_name = request_data['container_name'].strip();
    url = address + f"delete-container?container_name={container_name}"
    resp = req.get(url)
    return resp.text




@app.route('/')
def home():
    return render_template("index.html")


@app.route("/save-code",  methods = ['GET','POST'])
@cross_origin(supports_credentials=True)
def save_code():
    if request.method=="POST":
        request_data = request.get_json()
        code = request_data['code'].strip()
        container_name = request_data['container_name'].strip();

        with open("code/main.py", "w") as f:
            f.write(code)

        with open("tmp/output.txt", "w") as output:
            subprocess.run(f"sudo docker cp code/main.py {container_name}:/home/main.py", shell=True, stdout=output, stderr=output)

        with open("tmp/output.txt", "r") as file:
            val = file.read()

        d = {"success":True, "container_name":container_name, "response":val}
        return jsonify(d)



@app.route("/create-new-container")
@cross_origin(supports_credentials=True)
def create_new_container():
    request_data = request.args
    image_name = request_data['image_name']
    container_name = ''.join(random.choices(string.ascii_lowercase, k=8))

    if image_name=="hello-world":
        with open("tmp/output.txt", "w") as output:
            subprocess.run(f"sudo docker run --name {container_name} hello-world", shell=True, stdout=output, stderr=output)
    else: 
        with open("tmp/output.txt", "w") as output:
            subprocess.run(f"sudo docker run -d --name {container_name} --expose 80 --net nginx-proxy -e VIRTUAL_HOST={container_name}.codingchaska.school {image_name}", shell=True, stdout=output, stderr=output) 
    with open("tmp/output.txt", "r") as file:
        val = file.read()
    d = {"success":True,'container_name':container_name, "response":val}

    return jsonify(d)

@app.route("/delete-container")
@cross_origin(supports_credentials=True)
def delete_container():
    request_data = request.args
    container_name = request_data['container_name'].strip();
    with open("tmp/output.txt", "w") as output:
        subprocess.run(f"sudo docker kill {container_name};sudo docker rm -f {container_name}", shell=True, stdout=output, stderr=output)

    with open("tmp/output.txt", "r") as file:
        val = file.read()
    d = {"success":True, "container_name":container_name, "response":val}
    return jsonify(d)

@app.route("/show-containers")
@cross_origin(supports_credentials=True)
def show_containers():
    with open("tmp/output.txt", "w") as output:
        subprocess.run(f"sudo docker container ls -a", shell=True, stdout=output, stderr=output)

    with open("tmp/output.txt", "r") as file:
        val = file.read()
    d = {"success":True,"containers":val}

    return jsonify(d)

# main driver function
if __name__ == '__main__':
    app.run(debug=True)