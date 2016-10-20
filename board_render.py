from PIL import Image, ImageDraw, ImageFont
import math
from PyCatan import CatanBoard
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
		
		hexes_per_row = [
			3,
			4,
			5,
			4,
			3
		]
		rad = size[0] / 10
		
		# this is half the width of a hex
		half_width = math.sqrt(math.pow(rad, 2) - math.pow(rad * math.sin(math.pi / 6), 2))
		
		# this is the length of a line on the hex
		line_length = 2 * rad * math.sin(math.pi / 6)
		
		x_off = 0
		
		start = (
			size[0] / 2 - 1 * half_width, 
			size[1] / 2 - 2 * rad - line_length
		)
		
		# draws the board
		# for i in range(len(hexes_per_row)):
		for r in range(len(board.hexes)):
			
			# moves the next row of hexes over left or right to be aligned
			if r < 3:
				x_off -= half_width
				
			else:
				x_off += half_width
				
			for i in range(len(board.hexes[r])):
				
				x = i * 2 * half_width
				
				y = r * (rad + rad * math.sin(math.pi / 6))
		
				num = ""
				if board.hex_nums[r][i] != None:
					num = "{}".format(board.hex_nums[r][i])
	
				text_size = font.getsize(num)
		
				# draws the hex
				self.draw_hex(
					draw, 
					center=(start[0] + x_off + x, start[1] + y), 
					radius=rad, 
					color=colors[board.hexes[r][i]]
				)
				
				# draws the number token
				self.draw_bordered_text(
					num, 
					(
						start[0] + x_off + x - text_size[0] / 2,
						start[1] + y - text_size[1] / 2
					),
					3,
					font,
					draw
				)
				
		# the different colors for each player
		player_colors = [
			(239, 27, 0), # red
			(66, 64, 178), # blue
			(224, 224, 224), # white
			(71, 48, 0), # brown
			(43, 155, 75) #green
		]
		
		
		starting_coords = [
			# starts at the center of the board, then moves 1.5 hexes over
			size[0] / 2 - 3 * half_width,
			
			# starts at the center and moves 1.5 hexes up
			size[1] / 2 - 1.5 * line_length - 2 * rad
		]
		
		# draws the settlements/cities
		for r in range(len(board.points)):
			for i in range(len(board.points[r])):
			
				if board.points[r][i] != None:
					
					color = player_colors[board.points[r][i].owner]
					
					# moves each point over a bit
					if r < 3:
						x_off = i * half_width - r * half_width
					
					else:
						x_off = i * half_width - (5 - r) * half_width
					
					y_off = r * (line_length + 2 * rad - 1.5 * line_length)
					
					if r < 3:
						if i % 2 == 1:
							y_off -= 2 * rad - 1.5 * line_length
					
					else:
						if i % 2 == 0:
							y_off -= 2 * rad - 1.5 * line_length
										
					draw.ellipse(
						[
							(starting_coords[0] - 10 + x_off - 5, starting_coords[1] - 10 + y_off - 5),
							(starting_coords[0] + 20 + x_off, starting_coords[1] + 20 + y_off)
						],
						color
					)
		
		# draws the roads
		for road in board.roads:
			
			road.point_one
			road.point_two
			
			# gets the coordinates
			coords = []
			for i in [road.point_one, road.point_two]:
				
				place = [0, 0]
				
				# Gets the x coordinate
				place[0] = size[0] / 2 - 3 * half_width
				
				# moves over for each point
				place[0] +=  i[1] * half_width
				
				# moves back for each row
				if i[0] < 3:
					place[0] -= i[0] * half_width
				else:
					place[0] -= (5 - i[0]) * half_width
				
				# gets the y coordinate
				place[1] = size[1] / 2 - 2 * rad - 1.5 * line_length
				
				# moves up if the point is higher up
				if i[0] < 3:
					
					if i[1] % 2 == 1:
						place[1] -= rad - line_length / 2
						
				else:
					if i[1] % 2 == 0:
						place[1] -= rad - line_length / 2
						
				# moves the poin down for each row
				place[1] += i[0] * (2 * rad - line_length / 2)
						
				# adds the coord
				coords.append(place)
				
			for x in coords:
				
				draw.polygon(
					[
						(
							coords[0][0] + 5,
							coords[0][1] + 5
						),
						(
							coords[0][0] - 5,
							coords[0][1] - 5
						),
						(
							coords[1][0] - 5,
							coords[1][1] - 5
						),
						(
							coords[1][0] + 5,
							coords[1][1] + 5
						)
					],
					fill=player_colors[road.owner]
				)
				
		# draws the robber
			
					
		
		image.save("test.jpg")
	
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
	Draws a hex at the center specified
	
	draw: The PIL.ImageDraw.ImageDraw object to draw on
	center: A tuple with the x, y coordinates (x, y)
	radius: The distance from the center to one of its points
	color: The color to fill the hex
	'''
	def draw_hex(self, draw, center, radius, color):
	
		points = []
		
		deg = math.pi / 6
	
		# cycles through 6 times
		for i in range(6):
		
			# gets the x and y by forming a right angle triangle with the center and the points
			y = radius * math.sin(- deg + 2 * deg * i)
			
			x = math.sqrt(math.pow(radius, 2) - math.pow(y, 2))
			
			if i > 2:
				x *= -1
			
			points.append((center[0] + x, center[1] + y))
			
		
		draw.polygon(points, color, (0, 0, 0))
		
	
if __name__ == "__main__":
	import PyCatan
	
	b = BoardRenderer();
	c = PyCatan.CatanGame();
	
	c.add_settlement(player=0, r=0, i=0, is_starting=True)
	c.add_road(player=0, start=[0,0], end=[0, 1], is_starting=True)
	c.add_settlement(player=1, r=0, i=2, is_starting=True)
	c.add_settlement(player=2, r=0, i=5, is_starting=True)
	c.add_road(player=2, start=[0,5], end=[0, 4], is_starting=True)
	c.add_settlement(player=2, r=3, i=5, is_starting=True)
	c.add_road(player=2, start=[3,5], end=[3, 6], is_starting=True)
	c.add_settlement(player=2, r=4, i=1, is_starting=True)
	c.add_road(player=2, start=[4,1], end=[5, 0], is_starting=True)
	
	b.render_board(c.board, "test.jpg")