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
channel.queue_declare(queue="trylogin")

def on_request(ch, method, properties, body):
	while True:
		try:
			mydb = mysql.connector.connect(host=os.environ.get("MYSQL_HOST_NAME"), user=os.environ.get("MYSQL_USER"), passwd=os.environ.get("MYSQL_PASSWORD"), database=os.environ.get("MYSQL_DATABASE_NAME"))
			print("Connected to MYSQL!!!")
			break
		except:
			time.sleep(1)

	mycursor = mydb.cursor()
	comand = "SELECT * FROM Users WHERE Email =%s"
	Body = json.loads(body.decode("utf-8"))
	user = (Body["Email"],)

	mycursor.execute(comand, user)
	myresult = mycursor.fetchone()

	if not myresult:
		respostaJSON = {"Aceito":False,"Porque":"Usuario não encontrado"}

	else:
		if myresult[1] == Body["Password"]:
			respostaJSON = {"Aceito":True,"Code":myresult[3]}

		else:
			respostaJSON = {"Aceito":False,"Porque":"Usuario ou senha incorretos"}

	resposta = json.dumps(respostaJSON)

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="trylogin", on_message_callback=on_request)

channel.start_consuming()