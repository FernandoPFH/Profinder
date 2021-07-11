import json
import requests
import os
from time import sleep
from flask import Flask, request, render_template, session, jsonify
from flask_talisman import Talisman
from pymongo import MongoClient
from MongoDBFuncs import  newSessionishStart, newSessionishRequest, newSessionishUpdate, sessionishFileExist
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from email.message import EmailMessage

IP = os.environ.get("IP")
EMAIL = os.environ.get("EMAIL")
DEBUG = os.environ.get("DEBUG") == "true"
MongoURI = f"mongodb://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@{os.environ['MONGODB_HOSTNAME']}:27017"

mongoClient = MongoClient(MongoURI)

while True:
	try:
		mongoClient.list_database_names()
		print("Connected to MongoDB!!!")
		break
	except:
		sleep(1)

app = Flask(__name__)

if (DEBUG):
	PROTOCOLO = "http://"
	PORTA = ":5050"
else :
	PROTOCOLO = "https://"
	PORTA = "/api"

	Talisman(app)

URL = f"{PROTOCOLO}{IP}{PORTA}"

@app.route('/')
def main():
	return render_template("Main.html")

@app.route('/login/')
def login():
	return render_template("Login.html")

@app.route('/signup/')
def signup():
	return render_template("Signup.html")

@app.route('/account_data/<code>')
def prof_info(code):
	if (len(code) == 20):
		return render_template("MyAccount.html",UserCode=code,IP=IP)
	else:
		clientIPAdress = request.remote_addr
		return render_template("MyAccount.html",UserCode=newSessionishRequest(mongoClient,code,clientIPAdress,["UserCode"])["UserCode"],IP=IP)

@app.route('/create_project/<code>')
def create_project(code):
	return render_template("CreateProject.html",ProjectCode=code,IP=IP)

@app.route('/project/<code>')
def project(code):
	return render_template("Project.html",ProjectCode=code)

@app.route('/projects/')
def projects():
	return render_template("Projects.html")

@app.route("/send_data_for_login/<json_for_login>", methods=['GET','POST'])
def send_data_for_login(json_for_login):
	if request.method == 'GET':
		User = json.loads(json_for_login)

		response = json.loads(requests.get(f"{URL}/login/?email={User['Email']}&password={User['Password']}").text)

		if response["Aceito"]:
			clientIPAdress = request.remote_addr

			if User["sessionishClientId"] and sessionishFileExist(mongoClient,User["sessionishClientId"]):
				sessionishClientId = User["sessionishClientId"]

			else:
				sessionishClientId = newSessionishStart(mongoClient,clientIPAdress)

			newSessionishUpdate(mongoClient,sessionishClientId,clientIPAdress,{"Email":User["Email"],"Password":User["Password"],"UserCode":response["Code"]})

			response["sessionishClientId"] = sessionishClientId

			return jsonify(response)

		else:
			return jsonify(response)

	if request.method == 'POST':
		User = json.loads(json_for_login)

		response = json.loads(requests.post(f"{URL}/login/?email={User['Email']}&password={User['Password']}&name={User['Name']}&type={User['Type']}").text)

		if response["Aceito"]:
			clientIPAdress = request.remote_addr

			if User["sessionishClientId"] and sessionishFileExist(mongoClient,User["sessionishClientId"]):
				sessionishClientId = User["sessionishClientId"]

			else:
				sessionishClientId = newSessionishStart(mongoClient,clientIPAdress)

			newSessionishUpdate(mongoClient,sessionishClientId,clientIPAdress,{"Email":User["Email"],"Password":User["Password"],"UserCode":response["Code"]})

			response["sessionishClientId"] = sessionishClientId

			return jsonify(response)

		else:
			return jsonify(response)

@app.route("/try_login_by_session_data/<sessionishClientId>", methods=['GET'])
def try_login_by_session_data(sessionishClientId):
	if request.method == 'GET':
		if sessionishClientId and sessionishFileExist(mongoClient,sessionishClientId):
			clientIPAdress = request.remote_addr
			sessionishRequestResponse = newSessionishRequest(mongoClient,sessionishClientId,clientIPAdress,["Email","Password"])

			if type(sessionishRequestResponse) == type(str()):
				return jsonify({"Aceito":False})

			elif type(sessionishRequestResponse) == type(dict()):
				restHeader = "?"
				for key,value in sessionishRequestResponse.items():
					restHeader += key.lower() + "=" + value + "&"

				restHeader = restHeader[:-1]

				return requests.get(f"{URL}/login/{restHeader}").json()

			else:
				return jsonify({"Aceito":False})

		else:
			return jsonify({"Aceito":False})


@app.route("/send_data_for_account/<json_for_account>", methods=['GET','POST'])
def send_data_for_account(json_for_account):
	if request.method == 'GET':
		Data = json.loads(json_for_account)
		clientIPAdress = request.remote_addr
		try:
			usercode = Data["UserCode"]
		except:
			usercode = newSessionishRequest(mongoClient,Data["sessionishClientId"],clientIPAdress,["UserCode"])["UserCode"]
		try:
			Data["Method"] = "full" * (newSessionishRequest(mongoClient,Data["sessionishClientId"],clientIPAdress,["UserCode"])["UserCode"] == Data["UserCode"])
		except:
			Data["Method"] = ""

		if Data["Method"] == "full":
			sessionishRequestResponse = newSessionishRequest(mongoClient,Data["sessionishClientId"],clientIPAdress,["Email","Password","UserCode"])
			restHeader = "?"
			for key,value in sessionishRequestResponse.items():
				restHeader += key.lower() + "=" + value + "&"
			response = json.loads(requests.get(f"{URL}/account_data/{restHeader}method={Data['Method']}").text)
			response["IsYourCode"] = True
			return jsonify(response)
		else:
			response = json.loads(requests.get(f"{URL}/account_data/?usercode={usercode}&method={Data['Method']}").text)
			response["IsYourCode"] = False
			response["UserCode"] = usercode
			return jsonify(response)

	if request.method == 'POST':
		User = json.loads(json_for_account)
		clientIPAdress = request.remote_addr
		checkdata = newSessionishRequest(mongoClient,User["sessionishClientId"],clientIPAdress,["Email","Password","UserCode"])
		response = json.loads(requests.post(f"{URL}/account_data/?email_antigo={checkdata['Email']}&password_antigo={checkdata['Password']}&usercode={checkdata['UserCode']}&email_novo={User['Email']}&password_novo={User['Password']}&name={User['Name']}&type={User['Type']}").text)
		if response["Aceito"]:
			newSessionishUpdate(mongoClient,User["sessionishClientId"],clientIPAdress,{"Email":User["Email"],"Password":User["Password"]})
		return  jsonify(response)

@app.route("/update_image_account_data/<image_data>", methods = ['POST'])
def update_image_account_data(image_data):
	if request.method == 'POST':
		data = json.loads(image_data)
		clientIPAdress = request.remote_addr
		sessionishRequestResponse = newSessionishRequest(mongoClient,data["sessionishClientId"],clientIPAdress,["Email","Password","UserCode"])
		restHeader = "?"
		for key,value in sessionishRequestResponse.items():
			restHeader += key.lower() + "=" + value + "&"

		if int(data['updateProjectImage']):
			restHeader += f"projectcode={data['ProjectCode']}&"

		return requests.post(f"{URL}/update_image/{restHeader}updateprojectimage={str(data['updateProjectImage'])}&image={image_data}").json()

@app.route("/send_data_for_projects/<json_for_project>", methods=['GET','POST'])
def send_data_for_projects(json_for_project):
	if request.method == 'GET':
		data = json.loads(json_for_project)

		sessionishClientId = ""
		if "sessionishClientId" in data:
			if data["sessionishClientId"]:
				sessionishClientId = data["sessionishClientId"]

		if not sessionishFileExist(mongoClient,sessionishClientId):
			try:
				userCode = data["Usercode"]
			except:
				userCode = "-1"
			dataToReturn = json.loads(requests.get(f"{URL}/projects/?usercode={str(userCode)}&area={str(data['Area'])}&titulo={str(data['Titulo'])}&projectcode={str(data['ProjectCode'])}&publicado={str(data['Publicado'])}").text)
			for i in range(len(dataToReturn["Projetos"])):
				dataToReturn["Projetos"][i]["IsYourCode"] = False
			return jsonify(dataToReturn)

		else:
			try:
				userCode = data["Usercode"]
			except:
				try:
					clientIPAdress = request.remote_addr
					userCode = newSessionishRequest(mongoClient,sessionishClientId,clientIPAdress,["UserCode"])["UserCode"]
				except:
					userCode = "-1"

			dataToReturn = json.loads(requests.get(f"{URL}/projects/?usercode={userCode}&area={str(data['Area'])}&titulo={str(data['Titulo'])}&projectcode={str(data['ProjectCode'])}&publicado={str(data['Publicado'])}").text)
			if dataToReturn["Aceito"]:
				for i in range(len(dataToReturn["Projetos"])):
					dataToReturn["Projetos"][i]["IsYourCode"] = False
					for j in range(len(dataToReturn["Projetos"][i]["Users"])):
						if userCode in  dataToReturn["Projetos"][i]["Users"][j]:
							dataToReturn["Projetos"][i]["IsYourCode"] = True

			return jsonify(dataToReturn)

	if request.method == 'POST':
		data = json.loads(json_for_project)
		
		if data["sessionishClientId"] and sessionishFileExist(mongoClient,data["sessionishClientId"]):
			clientIPAdress = request.remote_addr
			sessionishRequestResponse = newSessionishRequest(mongoClient,data["sessionishClientId"],clientIPAdress,["UserCode"])

			createMethod = data["createMethod"]

			if bool(createMethod):
				urlStr = f"{URL}/projects/?createmethod={str(data['createMethod'])}&usercode={sessionishRequestResponse['UserCode']}&titulo={str(data['Titulo'])}&publicado={str(data['Publicado'])}"

				areaIndex = 1
				for area in data["Areas"]:
					urlStr += "&area" + str(areaIndex) + "=" + area
					areaIndex+=1

				userIndex = 1
				for user in data["Users"]:
					urlStr += "&user" + str(userIndex) + "=" + user
					userIndex+=1

				urlStr += f"&descr={data['Desc']}"

				return requests.post(urlStr).json()

			else:
				urlStr = f"{URL}/projects/?createmethod={str(data['createMethod'])}&projectcode={data['ProjectCode']}&titulo={str(data['Titulo'])}&publicado={str(data['Publicado'])}"

				areaIndex = 1
				for area in data["Areas"]:
					urlStr += "&area" + str(areaIndex) + "=" + str(area)
					areaIndex+=1

				userIndex = 1
				for user in data["Users"]:
					urlStr += "&user" + str(userIndex) + "=" + str(user)
					userIndex+=1

				urlStr += f"&descr={data['Desc']}"

				return requests.post(urlStr).json()

		else:
			return jsonify({"Aceito":False})

@app.route('/search_for_projects/<json_for_search>', methods=['GET'])
def search_for_projects(json_for_search):
	if request.method == 'GET':
		data = json.loads(json_for_search)
		
		urlStr = f"{URL}/searchforprojects/?"
		
		if len(data["Titulo"]) > 0:
			urlStr += "titulo="+str(data["Titulo"])
			
		if len(data["Tipo"]) > 0:
			urlStr +="&tipo="+data["Tipo"]

		areaIndex = 1
		for area in data["Areas"]:
			urlStr += "&area" + str(areaIndex) + "=" + str(area)
			areaIndex+=1

		return requests.get(urlStr).json()

@app.route('/data_to_contact_us/', methods=['POST'])
def data_to_contact_us():
	nome = request.args.get("name")
	email = request.args.get("email")
	menssagem = request.args.get("message")

	msg = Mail(from_email = "random@random.com",
			   to_emails = EMAIL,
			   subject = 'Profinder - Nos Contate - Nova Mensagem',
			   plain_text_content = f"Nome: {nome}\nEmail: {email}\nConteudo:\n{menssagem}"
	)

	sg = SendGridAPIClient("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")
	response = sg.send(msg)

@app.route("/send_data_for_projectssideinfos/", methods=['GET'])
def send_data_for_projectssideinfos():
	if request.method == 'GET':
		return requests.get(f"{URL}/projectssideinfos/").json()

@app.route("/send_data_for_userssideinfos/", methods=['GET'])
def send_data_for_userssideinfos():
	if request.method == 'GET':
		return requests.get(f"{URL}/userssideinfos/").json()

@app.route("/send_data_for_numberofusers/", methods=['GET'])
def send_data_for_numberofusers():
	if request.method == 'GET':
		return requests.get(f"{URL}/numberofusers/").json()

if __name__ == '__main__':
	app.run(host='0.0.0.0')