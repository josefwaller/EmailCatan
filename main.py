''' 
EmailCatan
Author: Josef Waller
Date: 13 October 2016
Purpose: Allows a game of Catan to be played entirely through emails between players
'''

import json
from bs4 import BeautifulSoup

''' libraries used for sending/receiving emails '''
import smtplib
import poplib
from email import parser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import quotequail

''' Libraries used for simulating the game '''
from PyCatan.catan_game import CatanGame
from PyCatan.catan_cards import CatanCards
from PyCatan.catan_board import CatanBoard

''' Sets up the main game '''
def main(admin_email):
	
	email = ""
	password = ""
	# reads the contents of the login file
	try:
		file = open("login.json", "r")
		login_info = json.loads(file.read())
		email = login_info['email']
		password = login_info['password']
		
	except:
		print("Error reading login file: Please make sure 'login.json' is a valid json file")
		return
	
	# attemps to connect to server
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(email, password)
	except:
		print("Error login in: Please check that the credentials in 'login.json' are valid")
		return
		
	try:
		# creates a new email
		msg = MIMEMultipart()
		msg['From'] = 'Catan Bot <{}>'.format(email)
		msg['To'] = admin_email
		msg['Subject'] = 'Setting up your Email Catan Game!'
		
		# creates new text
		body = MIMEText("""
		Welcome to setting up your EmailCatan game. Please read the instructions and don't mess up.
		
		Add players by replying 'ADD_PLAYER <their name> <theiremail@gmail.com>'
		Make a player a moderator by adding 'MOD' when adding them
		Start a new game with 'NEW_GAME'
		Load a game with 'LOAD_GAME <id>'
		
		Make sure to start the game only after you've added everybody (including yourself)
		
		Example:
		
		ADD_PLAYER Me myself@gmail.com MOD
		ADD_PLAYER Bob myfriend@gmail.com
		ADD_PLAYER Jake myenemy@gmail.com
		ADD_PLAYER Lucy myotherfriend@gmail.com
		NEW_GAME
		
		""", "plain")
		
		msg.attach(body)
		
		server.sendmail(email, admin_email, msg.as_string())
	except:
		print("Error sending mail: There was an error while sending the mail. " +
		"I don't really know why this would happen. Sporry :(")
		return
		
	game = None
	emails = []
	is_setting_up = True
		
	while True:
		e = get_new_emails(email, password)
		if e != []:
			if is_setting_up:
				
				# splits the body by spaces
				orders = e[0]['body'].split("\n")
				for o in orders:
					print(o)
					if o == "NEW_GAME":
						game = CatanGame(num_of_players=len(emails))
						
					if " " in o:
						print("Space detected")
						parts = o.split(" ")
						
						if parts[0] == "ADD_PLAYER":
							print("Adding player")
							name = parts[1]
							email = parts[2]
							
							emails.append({
								"name": name,
								"email": email
							})
							
				print(emails)
							
		
	server.quit()
	
''' Gets all the emails from the server and returns them as an array of dictionaries
	Ex:
		[
			{
				"from": "some_email"
				"subject": "some_subject"
				"body": "some_body"
			}
		]
'''
def get_new_emails(email, password):
		
	# connects the gmail
	pop_conn = poplib.POP3_SSL('pop.gmail.com')
	pop_conn.user(email)
	pop_conn.pass_(password)

	# Get messages from server:
	messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
				
	# decodes them
	messages = ["\n".join(m.decode("utf-8") for m in mssg[1]) for mssg in messages]
	
	to_return = []
	
	# Parse message intom an email object:
	messages = [parser.Parser().parsestr(mssg) for mssg in messages]
	
	for message in messages:
		
		# gets the body for each message
		body = ""
		
		for part in message.walk():
			
			if part.get_content_type() == "text/plain":
				body = part.get_payload()
				break
		
		# removes previous messages, if any
		new_body = quotequail.unwrap(body)
		
		if new_body != None:
			body = new_body['text_top']
					

		to_return.append({
			"from": message['From'],
			"subject": message['Subject'],
			"body": body
		})		
				
	# closes the server
	pop_conn.quit()
	
	# returns the messages
	return to_return;
	
if __name__ == "__main__":
	email = input("Please enter your email: ")
	print("You will be emailed about setting up a game")
	main(email)