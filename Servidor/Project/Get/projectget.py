import os
import pika
import time
import json
import mysql.connector

while True:
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST_NAME")))
		channel = connection.channel()
		print("Connected to Rabbitmq!!!")
		break
	except:
		time.sleep(1)
channel.queue_declare(queue="getproject")

def on_request(ch, method, properties, body):
	while True:
		try:
			mydb = mysql.connector.connect(host=os.environ.get("MYSQL_HOST_NAME"), user=os.environ.get("MYSQL_USER"), passwd=os.environ.get("MYSQL_PASSWORD"), database=os.environ.get("MYSQL_DATABASE_NAME"))
			print("Connected to MYSQL!!!")
			break
		except:
			time.sleep(1)

	mycursor = mydb.cursor()

	Body = json.loads(body.decode("utf-8"))
	comand = "SELECT * FROM Projects"


	WhereExits = False
	for item in Body:
		if Body[item] != "-1":
			WhereExits = True

	if WhereExits:
		comand += " WHERE "

		firstString = True
		for key, value in Body.items():
			if str(value) != "-1" and not key == "Areas" and not key == "UserCode":
				if firstString:
					firstString = False
					comand += str(key) + " = \"" + str(value) + "\""
				else:
					comand += " AND " + str(key) + " = \"" + str(value) + "\""

		if "UserCode" in Body:
			if Body["UserCode"] != "-1":
				comand = "SELECT * FROM Projects WHERE ProjectCode IN (SELECT ProjectCode FROM ProjectCodexUserCode WHERE UserCode = \"" + Body["UserCode"] + "\")"

	mycursor.execute(comand)
	myresult = mycursor.fetchall()

	if not myresult:
		respostaJSON = {"Aceito":False,"Porque":"Nenhum projeto encontrado"}

	else:
		respostaJSON = {"Aceito":True,"Projetos":[]}
		for linha in myresult:

			jsonLinha = {"ProjectCode":linha[0],"Titulo":linha[1],"Descr":linha[2],"Publicado":linha[3],"Image":linha[4]}

			comand = "SELECT Area FROM ProjectCodexArea WHERE ProjectCode = \"" + linha[0] + "\""
			mycursor.execute(comand)
			linhaResult = mycursor.fetchall()

			jsonLinha["Areas"] = []
			for area in linhaResult:
				jsonLinha["Areas"].append(area[0])

			comand = "SELECT Name,Type,Code FROM Users WHERE Code IN (SELECT UserCode FROM ProjectCodexUserCode WHERE ProjectCode = \"" + linha[0] + "\")"
			mycursor.execute(comand)
			linhaResult = mycursor.fetchall()

			jsonLinha["Users"] = []
			for user in linhaResult:
				jsonLinha["Users"].append(user)

			adicionarLinha = True

			if str(Body["Areas"]) != "-1":
				comand = "SELECT * FROM ProjectCodexArea WHERE ProjectCode = \"" + jsonLinha["ProjectCode"] + "\" AND Area IN ("

				for area in Body["Areas"]:
					comand += "\"" + area + "\","

				comand = comand[:-1] + ")"

				mycursor.execute(comand)
				jsonResult = mycursor.fetchall()

				if not jsonResult:
					adicionarLinha = False


			#elif str(Body["Users"]) != "-1":
			#	#TODO

			if adicionarLinha:
				respostaJSON["Projetos"].append(jsonLinha)

	resposta = json.dumps(respostaJSON)

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="getproject", on_message_callback=on_request)

channel.start_consuming()