from PIL import Image, ImageDraw, ImageFont
import math
from PyCatan import CatanBoard, CatanBuilding
from random import randint

class BoardRenderer:

	def __init__(self):
		pass

	def render_board(self, board, target):
		
		# sets the size of the image
		size = (800, 800)
		
		# creates a new image object
		image = Image.new("RGB", size)
		
		# creates a font object
		font = ImageFont.truetype("DroidSans.ttf", 40)
		
		# gets the draw for drawing things on its
		draw = ImageDraw.Draw(image)
		
		# draws the background
		draw.rectangle(
			[
				(0, 0),
				size
			],
			(137, 182, 255)
		)
		
		# different colors to use for the hexes
		colors = [None] * 6
		
		# adds the actualy colors
		colors[CatanBoard.HEX_HILLS] = (193, 48, 7)
		colors[CatanBoard.HEX_MOUNTAINS] = (112, 108, 107)
		colors[CatanBoard.HEX_PASTURE] = (86, 198, 55)
		colors[CatanBoard.HEX_FOREST] = (25, 109, 2)
		colors[CatanBoard.HEX_FIELDS] = (234, 234, 0)
		colors[CatanBoard.HEX_DESERT] = (255, 255, 178)
		
		# draws the board
		# for i in range(len(hexes_per_row)):
		for r in range(len(board.hexes)):
		

			for i in range(len(board.hexes[r])):
				self.draw_hex(draw, font, r, i, board.hex_nums[r][i], board, colors[board.hexes[r][i]])
				
		# the different colors for each player
		player_colors = [
			(239, 27, 0), # red
			(66, 64, 178), # blue
			(224, 224, 224), # white
			(71, 48, 0), # brown
			(43, 155, 75) #green
		]
		
		# draws the settlements/cities
		for r in range(len(board.points)):
			for i in range(len(board.points[r])):
			
				if board.points[r][i] != None:
					
					# gets the color
					color = player_colors[board.points[r][i].owner]

					# gets the coords
					coords = self.get_point_coords(r, i)

					radius = 10
					if board.points[r][i].type == CatanBuilding.BUILDING_CITY:
						radius = 15

					# draws
					draw.rectangle(
						[
							(
								coords[0] - radius, 
								coords[1] - radius
							),
							(
								coords[0] + 2 * radius,
								coords[1] + 2 * radius
							)
						],
						color
					)
		
		# draws the roads
		for road in board.roads:
			
			# gets the coordinates
			coords = []

			for i in [road.point_one, road.point_two]:
				
				place = self.get_point_coords(i[0], i[1])
						
				# adds the coord
				coords.append(place)
				
			points = []

			for i in range(len(coords)):

				points.append((
					coords[i][0] - 5 + 10 * i,
					coords[i][1] - 5 + 10 * i
				))
				points.append((
					coords[i][0] + 5 - 10 * i,
					coords[i][1] + 5 - 10 * i
				))
				
			# draws the road
			draw.polygon(
				points,
				fill=player_colors[road.owner]
			)

		# draws the harbors
		for h in board.harbors:

			# gets the pixel locations for each point
			point_one = self.get_point_coords(h.point_one[0], h.point_one[1])
			point_two = self.get_point_coords(h.point_two[0], h.point_two[1])

			# gets the average x and y between the harbor's two points
			x = abs(point_one[0] + point_two[0]) / 2
			y = abs(point_one[1] + point_two[1]) / 2

			# gets a new ImageFont Object
			font = ImageFont.truetype("DroidSans.ttf", 20)

			# moves the text away from the center of the board
			# this part is pretty complicated

			# gets the distance to the center of the board
			to_center = math.sqrt(math.pow(size[0] / 2 - x, 2) + math.pow(size[1] / 2 - y, 2))

			# gets the angle
			theta = math.asin((size[1] / 2 - y) / to_center)

			# moves away from center by adding to to_center and then recalculating the x and y
			to_center += 20

			y = size[1] / 2 + to_center * math.sin(theta)
			x = size[0] / 2 + to_center * math.cos(theta) * abs(size[0] / 2 - x) / (size[0] / 2 - x)

			# centers the text coords on the line
			text_size = font.getsize(h.get_type())
			x -= text_size[0] / 2
			y -= text_size[1] / 2

			self.draw_bordered_text(
				text=h.get_type(),
				coord=(x, y),
				w=1,
				font=font,
				draw=draw
			)
			

		# draws the robber
					
		
		image.save("test.jpg")
	
	'''
	Gets the pixel coordinates for a specific point
	
	r: The row of the point
	i: The index of the point
	'''
	def get_point_coords(self, r, i):
			
		size = (800, 800)
		rad = size[0] / 10
		
		# this is half the width of a hex
		half_width = math.sqrt(math.pow(rad, 2) - math.pow(rad * math.sin(math.pi / 6), 2))
		
		# this is the length of a line on the hex
		line_length = 2 * rad * math.sin(math.pi / 6)
		# creates array
		place = [0, 0]
		
		# Gets the x coordinate
		# starting at the middle of the board
		# and then moves over 1.5 hexes
		# so now its on the top-left point (0, 0)
		place[0] = size[0] / 2 - 3 * half_width
		
		# moves over half a hex for each point inbetween
		place[0] +=  i * half_width
		
		# Since the lower rows are shifted a bit to the left 
		# (or right, in the bottom half) we shift the coord 
		# over too
		if r < 3:

			# moves it half a hex left for each index
			place[0] -= r * half_width

		else:
			# moves it half a hex right for each index
			# since r > 2, it will be at most 2 half hexes
			place[0] -= (5 - r) * half_width
		
		# gets the y coordinate
		place[1] = size[1] / 2 - 2 * rad - 1.5 * line_length
		
		# moves up if the point is higher up
		if r < 3:
			
			if i % 2 == 1:
				place[1] -= rad - line_length / 2
				
		else:
			if i % 2 == 0:
				place[1] -= rad - line_length / 2
				
		# moves the poin down for each row
		place[1] += r * (2 * rad - line_length / 2)

		return place

	'''
	Draws text at the coords given with a black border
	
	text: What to draw
	coord: Where to draw the text (as a tuple (x, y))
	w: The width of the border
	font: The ImageFont Object
	draw: The ImageDraw Object
	'''
	def draw_bordered_text(self, text, coord, w, font, draw):
		
		# draws the black background
		for x in range(-1, 2):
			for y in range(-1, 2):
				
				if x != 0 or y != 0:
					draw.text(
						(coord[0] + w * x, coord[1] + w * y),
						text,
						fill=(0, 0, 0),
						font=font)
					
		# draws the white text in the middle
		draw.text(
			(coord[0], coord[1]),
			text,
			fill=(255, 255, 255),
			font=font)
		
		
		
	'''
	Draws a hex from the radius and index given
	
	draw: The PIL.ImageDraw.ImageDraw object to draw on
	font: The ImageFont Object for the hex number
	r: The row
	i: The index
	board: The CatanBoard Object
	hex_num: The number on this hex
	color: The color to fill the hex
	'''
	def draw_hex(self, draw, font, r, i, hex_num, board, color):
	
		points = []

		# adds the top points
		for x in range(3):
			if r < 3:
				
				coords = self.get_point_coords(r, 2 * i + x)

			else:

				coords = self.get_point_coords(r, 2 * i + x + 1)

			points.append((coords[0], coords[1]))

		# adds the bottom coords
		for x in range(2, -1, -1):

			if r < 2:
				coords = self.get_point_coords(r + 1, 2 * i + x + 1)

			else:
				coords = self.get_point_coords(r + 1, 2 * i + x)

			points.append((coords[0], coords[1]))
			
		# draws the hex
		draw.polygon(points, color, (0, 0, 0))


		# draws the number toekn
		num = ""
		if hex_num != None:
			num = "{}".format(hex_num)

		text_size = font.getsize(num)
		
		# draws the number token
		self.draw_bordered_text(
			num, 
			(
				(points[0][0] + points[2][0] - text_size[0]) / 2,
				(points[1][1] + points[4][1] - text_size[1]) / 2
			),
			3,
			font,
			draw
			)

		# draws the robber
		if board.robber[0] == r and board.robber[1] == i:
			radius = 10
			x = (points[0][0] + points[2][0]) / 2
			y = (points[1][1] + 2 * points[4][1]) / 3
			draw.ellipse(
				[
					(
						x - radius,
						y - radius
					),
					(
						x + 2 * radius,
						y + 2 * radius
					)
				],
				(0, 0, 0, 200)
			)
	
if __name__ == "__main__":
	from PyCatan import CatanGame, CatanCards
	
	b = BoardRenderer();
	c = CatanGame();
	
	c.add_settlement(player=0, r=0, i=0, is_starting=True)
	c.add_road(player=0, start=[0,0], end=[0, 1], is_starting=True)
	c.add_settlement(player=1, r=0, i=2, is_starting=True)
	c.add_settlement(player=2, r=0, i=5, is_starting=True)
	c.add_road(player=2, start=[0,5], end=[0, 4], is_starting=True)
	c.add_settlement(player=2, r=3, i=5, is_starting=True)
	c.players[2].add_cards([
		CatanCards.CARD_WHEAT,
		CatanCards.CARD_WHEAT,
		CatanCards.CARD_ORE,
		CatanCards.CARD_ORE,
		CatanCards.CARD_ORE,
	])
	c.add_city(player=2, r=3, i=5)
	c.add_road(player=2, start=[3,5], end=[3, 6], is_starting=True)
	c.add_settlement(player=2, r=4, i=1, is_starting=True)
	c.add_road(player=2, start=[4,1], end=[5, 0], is_starting=True)
	
	b.render_board(c.board, "test.jpg")