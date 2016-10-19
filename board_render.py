from PIL import Image, ImageDraw
import math

class BoardRenderer:

	def __init__(self):
		pass

	def render_board(self, board, target):
		
		# sets the size of the image
		size = (500, 500)
		
		# creates a new image object
		image = Image.new("RGB", size)
		
		# gets the draw for drawing things on its
		draw = ImageDraw.Draw(image)
		
		# draws a test hex
		self.draw_hex(draw, center=(250, 250), radius=50, color=(255, 0, 0))
		
		image.save("test.jpg")
		
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
			
			print(x, y)
			
		
		draw.polygon(points, color)
		
	
if __name__ == "__main__":
	import PyCatan
	
	b = BoardRenderer();
	c = PyCatan.CatanGame();
	
	b.render_board(c.board, "test.jpg")