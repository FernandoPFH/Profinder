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
channel.queue_declare(queue="searchforprojects")

def InnerJoin(comands,failSafe,columnToGet):
	if len(comands) == 0:
		return failSafe

	else:
		EMPS = []

		for comand in comands:
			EMPS.append({"EMPNumber":f"EMP{str(len(EMPS)+1)}","comand":f"SELECT EMP{str(len(EMPS)+1)}.{columnToGet} FROM ({comand}) AS EMP{str(len(EMPS)+1)}"})

		returnComand = ""

		if len(EMPS) > 1:
			returnComand = f"{EMPS[0]['comand']} INNER JOIN ({EMPS[1]['comand']}) AS {EMPS[1]['EMPNumber']} ON {EMPS[0]['EMPNumber']}.{columnToGet} = {EMPS[1]['EMPNumber']}.{columnToGet}"
			numberOfEMPS = len(EMPS) + 1
			del EMPS[:2]

			while len(EMPS) > 0:
				returnComand = f"{EMPS[0]['comand']} INNER JOIN ({returnComand}) AS EMP{str(numberOfEMPS)} ON {EMPS[0]['EMPNumber']}.{columnToGet} = EMP{str(numberOfEMPS)}.{columnToGet}"
				del EMPS[0]
				numberOfEMPS += 1

			returnComand = f"SELECT {columnToGet} FROM Projects WHERE {columnToGet} IN ({returnComand}) AND Publicado = 1"
			
			return returnComand

		else:
			return EMPS[0]["comand"]

def on_request(ch, method, properties, body):
	while True:
		try:
			mydb = mysql.connector.connect(host=os.environ.get("MYSQL_HOST_NAME"), user=os.environ.get("MYSQL_USER"), passwd=os.environ.get("MYSQL_PASSWORD"), database=os.environ.get("MYSQL_DATABASE_NAME"))
			print("Connected to MYSQL!!!")
			break
		except:
			time.sleep(1)

	Body = json.loads(body)

	comands = []

	if len(Body["Areas"]) > 0:
		comandAreas = "SELECT DISTINCT ProjectCodexArea.ProjectCode FROM ProjectCodexArea WHERE Area IN (\"" + '\",\"'.join(Body['Areas']) + "\")"
		comands.append(comandAreas)

	if len(Body["Titulo"]) > 0:
		comands.append(f"SELECT Projects.ProjectCode FROM Projects WHERE Titulo LIKE \'%{Body['Titulo']}%\'")

	if len(Body["Tipo"]) > 0:
		comands.append(f"SELECT DISTINCT ProjectCode FROM ProjectCodexUserCode WHERE UserCode IN (SELECT Code FROM Users WHERE Type = \"{Body['Tipo']}\")")

	comand = InnerJoin(comands,"SELECT ProjectCode FROM Projects WHERE Publicado=1","ProjectCode")

	mycursor = mydb.cursor()

	mycursor.execute(comand)
	myresult = mycursor.fetchall()

	if not myresult:
		respostaJSON = {"Aceito":False,"Porque":"Nenhum projeto encontrado"}

	else:
		Projetos = []
		for result in myresult:
			resultadoJSON = {"ProjectCode":result[0]}
			comand = f"SELECT Titulo,Image FROM Projects WHERE ProjectCode = \"{result[0]}\""
			mycursor.execute(comand)
			resultado = mycursor.fetchone()
			resultadoJSON["Titulo"] = resultado[0]
			resultadoJSON["Image"] = resultado[1]

			comand = f"SELECT Name,Type,Code FROM Users WHERE Code IN (SELECT UserCode FROM ProjectCodexUserCode WHERE ProjectCode = \"{result[0]}\")"
			mycursor.execute(comand)
			resultadoJSON["Membros"] = mycursor.fetchall()

			comand = f"SELECT Area FROM ProjectCodexArea WHERE ProjectCode = \"{result[0]}\""
			mycursor.execute(comand)
			resultadoJSON["Areas"] = []
			for area in mycursor.fetchall():
				resultadoJSON["Areas"].append(area[0])

			Projetos.append(resultadoJSON)

		respostaJSON = {"Aceito":True,"Projetos":Projetos}

	resposta = json.dumps(respostaJSON)

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="searchforprojects", on_message_callback=on_request)

channel.start_consuming()