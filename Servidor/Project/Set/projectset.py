import os
import pika
import time
import json
import mysql.connector
from random import randint

while True:
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST_NAME")))
		channel = connection.channel()
		print("Connected to Rabbitmq!!!")
		break
	except:
		time.sleep(1)
channel.queue_declare(queue="setproject")

def generate_code(mydb,mycursor):
	run = True

	while run:
		code = ""
		for x in range(20):
			isAInvalidNumber = True
			while isAInvalidNumber:
				integer = randint(33,126)

				if integer not in {34,35,36,37,38,40,41,43,44,47,58,59,60,61,62,63,64,91,92,93,94,96,123,124,125}:
					isAInvalidNumber = False

			code += chr(integer)

		comand = "SELECT * FROM Projects WHERE ProjectCode =%s"

		mycursor.execute(comand, (code,))
		myresult = mycursor.fetchone()

		if not myresult:
			run = False

	return code

def check_for_changes(areasAntigas,areasNovas):
	areasAntigas_temp = areasAntigas.copy()
	areasNovas_temp = areasNovas.copy()

	for areaNova in areasNovas:
		if areaNova in areasAntigas_temp:
			areasAntigas_temp.remove(areaNova)

	for areaAntiga in areasAntigas:
		if areaAntiga in areasNovas_temp:
			areasNovas_temp.remove(areaAntiga)

	return areasAntigas_temp, areasNovas_temp

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

	if True:
		if Body["CreateMethod"]:
			comand_insert = "INSERT INTO ProjectCodexArea (ProjectCode,Area) VALUES (%s,%s)"
			projectCode = generate_code(mydb,mycursor)
			for area in Body["Areas"]:
				info = (projectCode,area)
				mycursor.execute(comand_insert,info)
				mydb.commit()
				
			comand_insert = "INSERT INTO ProjectCodexUserCode (ProjectCode,UserCode) VALUES (%s,%s)"
			for user in Body["Users"]:
				info = (projectCode,user)
				mycursor.execute(comand_insert,info)
				mydb.commit()

			comand_insert = "INSERT INTO Projects (ProjectCode,Titulo,Descr,Publicado) VALUES (%s,%s,%s,%s)"
			info = (projectCode,Body["Titulo"],Body["Descr"],Body["Publicado"])

		else:
			projectCode = Body["ProjectCode"]
			comand_insert = "SELECT Area FROM ProjectCodexArea WHERE ProjectCode = \"" + projectCode + "\""
			mycursor.execute(comand_insert)
			areasResult = mycursor.fetchall()
			areasResultAntigas = []
			for area in areasResult:
				areasResultAntigas.append(area[0])
			
			areasAntigas,areasNovas= check_for_changes(areasResultAntigas,Body["Areas"])

			if len(areasAntigas) > 0:
				command_remove = "DELETE FROM ProjectCodexArea WHERE ProjectCode = \"" + projectCode + "\" AND Area IN ("
				for areaAntiga in areasAntigas:
					command_remove += "\"" + areaAntiga + "\","

				command_remove = command_remove[:-1] + ")"

				mycursor.execute(command_remove)
				mydb.commit()

			if len(areasNovas) > 0:
				comand_insert = "INSERT INTO ProjectCodexArea (ProjectCode,Area) VALUES (%s,%s)"
				infos = []
				for areaNova in areasNovas:
					infos.append((projectCode,areaNova))
				
				mycursor.executemany(comand_insert,infos)
				mydb.commit()

			comand_insert = "SELECT UserCode FROM ProjectCodexUserCode WHERE ProjectCode = \"" + projectCode + "\""
			mycursor.execute(comand_insert)
			usersResult = mycursor.fetchall()
			usersResultAntigas = []
			for user in usersResult:
				usersResultAntigas.append(user[0])

			usersAntigas,usersNovas= check_for_changes(usersResultAntigas,Body["Users"])

			if len(usersAntigas) > 0:
				command_remove = "DELETE FROM ProjectCodexUserCode WHERE ProjectCode = \"" + projectCode + "\" AND UserCode IN ("
				for userAntiga in usersAntigas:
					command_remove += "\"" + userAntiga + "\","

				command_remove = command_remove[:-1] + ")"

				mycursor.execute(command_remove)
				mydb.commit()

			if len(usersNovas) > 0:
				comand_insert = "INSERT INTO ProjectCodexUserCode (ProjectCode,UserCode) VALUES (%s,%s)"
				infos = []
				for userNova in usersNovas:
					infos.append((projectCode,userNova))
				
				mycursor.executemany(comand_insert,infos)
				mydb.commit()

			comand_insert = "UPDATE Projects SET Titulo = %s, Descr = %s, Publicado = %s WHERE ProjectCode = %s"
			info = (Body["Titulo"],Body["Descr"],Body["Publicado"],projectCode)

		mycursor.execute(comand_insert,info)
		mydb.commit()
		respostaJSON = {"Aceito":True,"ProjectCode":projectCode}
	else:
		respostaJSON = {"Aceito":False}

	resposta = json.dumps(respostaJSON)

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="setproject", on_message_callback=on_request)

channel.start_consuming()