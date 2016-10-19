''' 
EmailCatan
Author: Josef Waller
Date: 13 October 2016
Purpose: Allows a game of Catan to be played entirely through emails between players
'''

import json

import poplib


''' Libraries used for simulating the game '''
from PyCatan.catan_game import CatanGame
from PyCatan.catan_cards import CatanCards
from PyCatan.catan_board import CatanBoard

''' see email_manager.py '''
from email_manager import EmailManager

# gets some templates for emails from external files
help_email = open("email_templates/help.txt", "r").read()
invite_email = open("email_templates/invite.txt", "r").read()
start_email = open("email_templates/started.txt", "r").read()
start_first_player_email = open("email_templates/started_first_player.txt", "r").read()
error_email = open("email_templates/error.txt", "r").read()

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
		
	games = [
		{
			"game": CatanGame(),
			"state": 1,
			"turn": 0,
			"players": [
				{
					"name": "Josef",
					"email": "josef@siriusapplications.com",
					"confirmed": False
				}
			]
		}
	]
	emails = []
	
	CONFIRMING = 0
	BUILDING_PHASE = 1
	PLAYING = 2
		
	while True:
	
		try:
			emails = manager.get_emails()
		except poplib.error_proto:
			pass

		for e in emails:
		
			print("Received an email from {}".format(e['from']))


			this_game = None
			this_player = None

			for i in range(len(games)):
				for x in range(len(games[i]['players'])):
					
					print("Comparing {} and {}".format(games[i]['players'][x]['email'], e['from']))
				
					if games[i]['players'][x]['email'] == e['from']:
						
						this_game = i
						this_player = x

			players = []

			# splits the body by newlines
			orders = e['body'].split("\n")
			for o in orders:

				# checks if the user needs help with orders first
				if o.replace(" ", "") == "HELP":
					manager.send_email(
						to=e['from'],
						subject="Help with EmailCatan",
						contents=help_email
					)

				# creates a new game
				if this_game == None:
					
					if o.lower() == "new_game":
					
						print("Creating a new game")
					
						games.append({
							"game": CatanGame(num_of_players=len(players)),
							"state": CONFIRMING,
							"turn": 0,
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
								contents=invite_email.format(name=players[i]['name'], player_names=", ".join(player_names)))
						
					if " " in o:
						parts = o.split(" ")
						
						if parts[0].lower() == "add_player":
							
							players.append({
								"name": parts[1],
								"email": parts[2],
								"confirmed": False
							})
							
							print("Added player {name}, <{email}>".format(name=parts[1], email=parts[2]))

				# if the game already exists
				else:

					print("Received email from an existing game")
					
					# checks which state it is in
					if games[this_game]['state'] == CONFIRMING:

						# checks if the playe agreed to playe
						if e['body'].lower() == 'yes':
							
							# marks them as ready to playe
							games[this_game]['players'][this_player]['confirmed'] = True

							# checks if everyone has confirmed
							all_confirmed = False

							for p in games[this_game]['players']:
								if not p['confirmed']:

									all_confirmed = True
									break

							if all_confirmed:
							
								print("All players have agreed to play")
								
								games[this_game]['state'] = BUILDING_PHASE
							
								# sends mail to all the players
								for i in range(1, len(games[this_game]['players'])):
									
									p = games[this_game]['players'][i]
									
									manager.send_email(
										to=p['email'],
										subject='The Game of Catan has started',
										contents=start_email.format(games[this_game]['players'][0]['name'])
								)
								
								# sends the email to the first player
								p = games[this_game]['players'][0]
								manager.send_email(
									to=p['email'],
									subject='It is your turn to play',
									contents=start_first_player_email
								)
								
								
					elif games[this_game]['state'] == BUILDING_PHASE:
						
						print("Game is in the building phase")
						if " " in o:
							p = o.split(" ")
							
							if p[0] == "BUILD_SETTLEMENT":
								
								# gets the coords for the first point
								settle_coords = [int(x) for x in p[1].split(",")]
								
								# gets the coords for the second point
								road_coords = [int(x) for x in p[3].split(",")]
								
								# checks they are connected
								points = games[this_game]['game'].board.get_connected_points(
									settle_coords[0], 
									settle_coords[1])
									
								valid_point = False
								for p in points:
									if road_coords == p or road_coords == p.reverse():
										valid_point = True
										break
										
								if not valid_point:
									manager.send_email(
										to=e['from'],
										subject="Invalid road placement",
										contents=error_email.format(errors="- Invalid Road placement")
									)
								else:
									
									# adds the settlement
									games[this_game]['game'].add_settlement(
										player=this_player,
										r=settle_coords[0],
										i=settle_coords[1],
										is_starting=True
										
									)
									
									# adds the road
									games[this_game]['game'].add_road(
										player=this_player,
										start=settle_coords,
										end=road_coords,
										is_starting=True
									)
									
									# sends the next player the prompt
									g = games[this_game]
									g['turn'] = (g['turn'] + 1) % len(g['players'])
									
									manager.send_email(
										to=g['players'][g['turn']]['email'],
										subject="It is your turn to build your first settlements",
										contents=
"""
	It is now your turn to build your starting settlements.
	Ther will be other stuff here to, but its not added yet.
""")
					
					elif games[this_game]['state'] == PLAYING:
						
						if " " in o:
							p = o.split(" ")
							
							if p[0] == "BUILD":
							
								if p[1] == "SETTLEMENT":
								
									# the coords will be in p[3] as x,x
									
									coords = p[3].split(',')
									
									for c in coords:
										c = int(c)
										
									games[this_game]['game'].add_settlement(
										player=this_player,
										r = coords[0],
										i = coords[1]
									)
								
				
	manager.server.quit()		
	
	
if __name__ == "__main__":
	# email = input("Please enter your email: ")
	# print("You will be emailed about setting up a game")
	main()