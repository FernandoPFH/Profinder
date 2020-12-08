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

channel.queue_declare(queue="newlogin")

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

		comand = "SELECT * FROM Users WHERE Code =%s"

		mycursor.execute(comand, (code,))
		myresult = mycursor.fetchone()

		if not myresult:
			run = False

	return code

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

	try:
		code = Body["UserCode"]

		comand = "SELECT * FROM Users WHERE Code =%s"
		user = (Body["UserCode"],)

		mycursor.execute(comand, user)
		myresult = mycursor.fetchone()

		if not myresult:
			respostaJSON = {"Aceito":False,"Porque":"Usuario não encontrado"}

		else:
			comand_insert = "UPDATE Users SET Email = %s, Password = %s, Type = %s, Name = %s WHERE Code = %s"
			code = generate_code(mydb,mycursor)
			info = (Body["Email"],Body["Password"],Body["Type"],Body["Name"],Body["UserCode"])
			mycursor.execute(comand_insert,info)
			mydb.commit()
			respostaJSON = {"Aceito":True}

	except:
		comand = "SELECT * FROM Users WHERE Email =%s"
		user = (Body["Email"],)

		mycursor.execute(comand, user)
		myresult = mycursor.fetchone()

		if not myresult:
			code = generate_code(mydb,mycursor)
			comand_insert = "INSERT INTO Users (Email, Password, Type, Code, Name) VALUES (%s, %s, %s, %s, %s)"
			info = (Body["Email"],Body["Password"],Body["Type"],code,Body["Name"])
			mycursor.execute(comand_insert,info)
			mydb.commit()
			respostaJSON = {"Aceito":True,"Type":Body["Type"],"Code":code}

		else:
			respostaJSON = {"Aceito":False,"Porque":"Email já resgistrado"}

	resposta = json.dumps(respostaJSON)

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="newlogin", on_message_callback=on_request)

channel.start_consuming()