''' 
EmailCatan
Author: Josef Waller
Date: 13 October 2016
Purpose: Allows a game of Catan to be played entirely through emails between players
'''

import json


''' Libraries used for simulating the game '''
from PyCatan.catan_game import CatanGame
from PyCatan.catan_cards import CatanCards
from PyCatan.catan_board import CatanBoard

''' see email_manager.py '''
from email_manager import EmailManager

''' Sets up the main game '''
def main():
	

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
	manager = EmailManager(email, password)
		
	# try:

		# manager.send_email(
		# 	admin_email,
		# 	'Setting up your Email Catan Game',
		# 	"""
		# 	Welcome to setting up your EmailCatan game. Please read the instructions and don't mess up.
			
		# 	Add players by replying 'ADD_PLAYER <their name> <theiremail@gmail.com>'
		# 	Make a player a moderator by adding 'MOD' when adding them
		# 	Start a new game with 'NEW_GAME'
		# 	Load a game with 'LOAD_GAME <id>'
			
		# 	Make sure to start the game only after you've added everybody (including yourself)
			
		# 	Example:
			
		# 	ADD_PLAYER Me myself@gmail.com MOD
		# 	ADD_PLAYER Bob myfriend@gmail.com
		# 	ADD_PLAYER Jake myenemy@gmail.com
		# 	ADD_PLAYER Lucy myotherfriend@gmail.com
		# 	NEW_GAME

		# 	""")

	# except Exception as e:
	# 	print(e)
	# 	print("Error sending mail: There was an error while sending the mail. " +
	# 	"I don't really know why this would happen. Sorry :(")
	# 	return
		
	games = []
	emails = []
	CONFIRMING = 0
		
	while True:
		e = manager.get_emails()
		if e != []:

			this_game = None
			this_player = None

			for i in range(len(games)):
				for x in range(len(games[i]['players'])):
					print(games[i]['players'][x]['email'])
					if games[i]['players'][x]['email'] == e[0]['from']:
						
						this_game = i
						this_player = x
						print("ASDF")

			players = []

			# splits the body by spaces
			orders = e[0]['body'].split("\n")
			for o in orders:
				print(o)

				# creates a new game
				if this_game == None:
					
					if o == "NEW_GAME":
						games.append({
							"game": CatanGame(num_of_players=len(players)),
							"state": CONFIRMING,
							"players": players
						})

						# sends an email to each player
						for i in range(len(players)):

							player_names = []

							for x in range(len(players)):
								if x != i:
									player_names.append(players[x]['name'])

							manager.send_email(
								to=players[i]['email'],
								subject='You\'ve been invited to play The Settlers of Catan',
								contents="""
								
									{name}, you have been invited to player The Settlers of Catan through email.
									You will be playing with {player_names}

									To accept, reply 'YES'
									To decline, reply 'NO'
									Otherwise you will confuse me.

									Thanks,
									Catan Bot

								""".format(name=players[i]['name'], player_names=",".join(player_names)))
						print(games)
						
					if " " in o:
						parts = o.split(" ")
						
						if parts[0] == "ADD_PLAYER":
							
							players.append({
								"name": parts[1],
								"email": parts[2],
								"confirmed": False
							})

				# if the game already exists
				else:

					print("Exostomg game")

					# checks which stage it is in
					if game[this_game]['stage'] == CONFIRMING:

						# checks if the playe agreed to playe
						if e['body'] == 'YES':
							
							# marks them as ready to playe
							game[this_game]['players'][this_player]['confirmed'] = True

							# checks if everyone has confirmed
							all_confirmed = False

							for p in game[this_game]['players']:
								if not p['confirmed']:

									all_confirmed = True
									break

							if all_confirmed:
								# sends mail to all the players
								for p in game[this_game]['players']:
									manager.send_email(
										to=p['email'],
										subject='The Game of Catan has started',
										contents=
"""
Everyone hase agreed to play and the game has begun.
It is {}'s turn first.
""".format(game[this_game]['players'][0]['name'])
								)

				
	manager.server.quit()		
	
	
if __name__ == "__main__":
	# email = input("Please enter your email: ")
	# print("You will be emailed about setting up a game")
	main()