import os
import pika
import uuid
import json
from flask import Flask, request
import time
app = Flask(__name__)

while True:
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST_NAME")))
		connection.channel()
		print("Connected to Rabbitmq!!!")
		break
	except:
		time.sleep(1)

class Mensagem(object):
	def __init__(self, queue):
		self.queue = queue
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST_NAME")))
		self.channel = self.connection.channel()
		result = self.channel.queue_declare(queue='', exclusive=True)
		self.callback_queue = result.method.queue
		self.channel.basic_consume(queue=self.callback_queue,on_message_callback=self.on_response,auto_ack=True)

	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body.decode("utf-8")

	def call(self, mensagem):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='',routing_key=self.queue,properties=pika.BasicProperties(reply_to=self.callback_queue,correlation_id=self.corr_id),body=mensagem)
		while self.response is None:
			self.connection.process_data_events()
		return self.response

def try_login(User):
	mensagem = Mensagem(queue="trylogin")
	return mensagem.call(mensagem=json.dumps(User))

@app.route('/')
def hello_world():
	return "Ola"

@app.route('/login/', methods = ['GET','POST'])
def login():
	if request.method == 'GET':
		User = {"Email":request.args.get('email'),"Password":request.args.get('password')}
		return try_login(User)

	if request.method == 'POST':
		NewUser = {"Email":request.args.get('email'),"Password":request.args.get('password'),"Name":request.args.get('name'),"Type":request.args.get('type')}
		mensagem = Mensagem(queue="newlogin")
		return mensagem.call(mensagem=json.dumps(NewUser))

@app.route('/account_data/', methods = ['GET','POST'])
def account_data():
	if request.method == 'GET':
		if request.args.get("method") == "full":
			checkdata = {"Email":request.args.get("email"),"Password":request.args.get("password")}
			response = json.loads(try_login(checkdata))
			usercode = request.args.get('usercode')
			if response["Aceito"] and (response["Code"] == usercode):
				mensagem = Mensagem(queue="get_account_data")
				data = {"method":"full","UserCode":usercode}
				return mensagem.call(mensagem=json.dumps(data))
			else:
				return json.dumps({"Aceito":False,"Porque":"Erro ao comparar a credenciais"})

		else:
			mensagem = Mensagem(queue="get_account_data")
			data = {"method":"parc","UserCode":request.args.get('usercode')}
			return mensagem.call(mensagem=json.dumps(data))

	if request.method == 'POST':
		checkdata = {"Email":request.args.get("email_antigo"),"Password":request.args.get("password_antigo")}
		response = json.loads(try_login(checkdata))
		usercode = request.args.get('usercode')
		if response["Aceito"] and (response["Code"] == usercode):
			mensagem = Mensagem(queue="newlogin")
			User = {"UserCode":usercode,"Email":request.args.get("email_novo"),"Password":request.args.get("password_novo"),"Type":request.args.get("type"),"Name":request.args.get('name')}
			return mensagem.call(mensagem=json.dumps(User))
		else:
			return json.dumps({"Aceito":False,"Porque":"Erro"})

@app.route("/update_image/", methods = ['POST'])
def update_image():
	if request.method == 'POST':
		checkdata = {"Email":request.args.get("email"),"Password":request.args.get("password")}
		response = json.loads(try_login(checkdata))
		usercode = request.args.get('usercode')
		updateProjectImage = int(request.args.get('updateprojectimage'))
		if response["Aceito"] and (response["Code"] == usercode):
			mensagem = Mensagem(queue="set_account_data")
			imageJSON = json.loads(request.args.get('image'))
			imageurl = f"http://{imageJSON['IP']}:5100/{imageJSON['urlprefix']}/{imageJSON['filename']}".replace(" ","%20")
			Infos = {"UserCode":response["Code"],"Image":imageurl}
			if updateProjectImage:
				Infos["ProjectCode"] = request.args.get('projectcode')
			return mensagem.call(mensagem=json.dumps(Infos))
		else:
			return json.dumps({"Aceito":False,"Porque":"Erro"})

@app.route('/projects/', methods = ['GET','POST'])
def projects():
	if request.method == 'GET':
		ProjectInfo = {"ProjectCode":request.args.get("projectcode"),"Titulo":request.args.get("titulo"),"UserCode":request.args.get("usercode"),"Publicado":int(request.args.get("publicado"))}

		indexOfAreas = 1
		ProjectInfo["Areas"] = []
		Area = request.args.get("area"+str(indexOfAreas))
		while Area:
			ProjectInfo["Areas"].append(Area)
			indexOfAreas += 1
			Area = request.args.get("area"+str(indexOfAreas))
		if len(ProjectInfo["Areas"]) == 0:
			ProjectInfo["Areas"] = "-1"

		mensagem = Mensagem(queue="getproject")
		return mensagem.call(mensagem=json.dumps(ProjectInfo))

	if request.method == 'POST':
		createMethod = int(request.args.get("createmethod"))

		ProjectInfo = {"Titulo":request.args.get("titulo"),"Descr":request.args.get("descr").replace(" !@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@! ","/"),"CreateMethod":createMethod,"Publicado":int(request.args.get("publicado"))}

		indexOfAreas = 1
		ProjectInfo["Areas"] = []
		Area = request.args.get("area"+str(indexOfAreas))
		while Area:
			ProjectInfo["Areas"].append(Area)
			indexOfAreas += 1
			Area = request.args.get("area"+str(indexOfAreas))

		indexOfUsers = 1
		ProjectInfo["Users"] = []
		User = request.args.get("user"+str(indexOfUsers))
		while User:
			ProjectInfo["Users"].append(User)
			indexOfUsers += 1
			User = request.args.get("user"+str(indexOfUsers))

		if not createMethod:
			ProjectInfo["ProjectCode"] = request.args.get("projectcode")

		mensagem = Mensagem(queue="setproject")
		return mensagem.call(mensagem=json.dumps(ProjectInfo))

@app.route('/searchforprojects/', methods = ['GET'])
def searchforprojects():
	if request.method == 'GET':
		ProjectInfo = {"Titulo":request.args.get("titulo"),"Tipo":request.args.get("tipo")}

		if not ProjectInfo["Titulo"]:
			ProjectInfo["Titulo"] = ""

		if not ProjectInfo["Tipo"]:
			ProjectInfo["Tipo"] = ""

		indexOfAreas = 1
		ProjectInfo["Areas"] = []
		Area = request.args.get("area"+str(indexOfAreas))
		while Area:
			ProjectInfo["Areas"].append(Area)
			indexOfAreas += 1
			Area = request.args.get("area"+str(indexOfAreas))
			
		mensagem = Mensagem(queue="searchforprojects")
		return mensagem.call(mensagem=json.dumps(ProjectInfo))

@app.route('/projectssideinfos/', methods = ['GET'])
def projectssideinfos():
	if request.method == 'GET':
		mensagem = Mensagem(queue="getprojectssideinfos")
		return mensagem.call(mensagem="")

@app.route('/userssideinfos/', methods = ['GET'])
def userssideinfos():
	if request.method == 'GET':
		mensagem = Mensagem(queue="getuserssideinfos")
		return mensagem.call(mensagem="")

if __name__ == '__main__':
	app.run(host='0.0.0.0')