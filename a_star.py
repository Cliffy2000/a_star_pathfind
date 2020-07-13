import math
import time
import numpy as np
import tkinter as tk
from tkinter import messagebox

import pygame
pygame.init()


PIXEL_SIZE = 20
BG_COLOR = (40, 40, 40)
WHITE = (255, 255, 255)
GREY = (220, 220, 220)
RED = (255, 50, 50)
GREEN = (35, 190, 35)
DARK_GREEN = (15, 165, 15)
BLUE = (30, 30, 170)


class pixel:
	# This class is for every pixel on the grid.

	def __init__(self, i, j):
		self.size = PIXEL_SIZE
		self.i = i
		self.j = j
		self.x = i * self.size
		self.y = j * self.size
		self.active = True		# This variable is to track if the pixel is accessible

		self.g_score = 0
		self.h_score = 0
		self.f_score = 0
		self.previous = None


	def draw(self, screen, color, border=0):
		# Set border to 1 to draw without filling the center
		shape = (self.x, self.y, self.size, self.size)
		pygame.draw.rect(screen, color, shape, border)
		pygame.display.update()


	def update_next(self, next, grid):
		# Checks if the current pixel could lead to another one and if so change the scores of the other pixel.
		distance = math.sqrt((self.i - next.i)**2 + (self.j - next.j)**2)
		if next.g_score > (self.g_score + distance) or next.g_score == 0:
			next.g_score = self.g_score + distance
			next.previous = grid[self.i][self.j]
			next.f_score = next.g_score + next.h_score


	def check_neighbors(self, grid, screen):
		# Returns all of the coordinates of the active pixels that are adjacent to the current one.
		self.active = False
		neighbors = []
		for i in range(3):
			for j in range(3):
				if grid[self.i+i-1][self.j+j-1].active:
					neighbors.append([self.i+i-1, self.j+j-1])
					self.update_next(grid[self.i+i-1][self.j+j-1], grid)

		return neighbors



class submission:
	# Used to simplify the entries of tkinter windows.

	def __init__(self, window):
		self.val = []
		self.entry = tk.Entry(window)



def submit_grid():
	# Processes the input from the grid size query.
	val = grid_size.entry.get()
	grid_size.val = [int(i) for i in val.split(',')]

	grid_window.quit()
	grid_window.destroy()


def submit_points():
	# Processes the input from the start and end point queries.
	start = start_point.entry.get()
	end = end_point.entry.get()
	start_point.val = [int(i) for i in start.split(',')]
	end_point.val = [int(i) for i in end.split(',')]

	point_window.quit()
	point_window.destroy()


def initial_prompt():
	# Gives instructions on how to use the path finder and asks for the desired size of the grid
	root = tk.Tk()
	root.withdraw()
	tk.messagebox.showinfo(title='Path Finder', message='How to use this pathfinder:\n     Type in the coordinates separated by a comma.\n     Left click/drag on the grid to add obstacles.\n     Press space bar or enter to start the A* algorithm.')

	global grid_size		# Have to use global variables to obtain the results from the entry
	global grid_window

	grid_window = tk.Tk(className='Creating map')
	grid_window.geometry('270x160')
	grid_size = submission(grid_window)

	prompt = tk.Label(grid_window, text='Size of grid: x,y') 
	submit = tk.Button(grid_window, text='Submit', command=submit_grid)

	prompt.place(relx=0.5, rely=0.25, anchor='center')
	grid_size.entry.place(relx=0.5, rely=0.4, anchor='center')
	submit.place(relx=0.5, rely=0.6, anchor='center')
	grid_window.update()
	tk.mainloop() 


def prompt_start_end():
	# Asks the user for the desired locations of the start and end points
	global start_point
	global end_point
	global point_window

	point_window = tk.Tk(className='Defining start and end points')
	point_window.geometry('330x160')
	start_point = submission(point_window)
	end_point = submission(point_window)

	start_prompt = tk.Label(point_window, text='Starting point: x,y')
	end_prompt = tk.Label(point_window, text='Ending point: x,y')
	submit = tk.Button(point_window, text='Submit', command=submit_points)

	start_prompt.place(relx=0.25, rely=0.25, anchor='center')
	end_prompt.place(relx=0.75, rely=0.25, anchor='center')
	start_point.entry.place(relx=0.25, rely=0.4, anchor='center')
	end_point.entry.place(relx=0.75, rely=0.4, anchor='center')
	submit.place(relx=0.5, rely=0.6, anchor='center')
	point_window.update()
	tk.mainloop()


def heuristic(pixel1, pixel2):
	# Calculates the direct distance between two pixels
	return math.sqrt((pixel1.i - pixel2.i)**2 + (pixel1.j - pixel2.j)**2)


def no_path_alert():
	root = tk.Tk()
	root.withdraw()
	tk.messagebox.showwarning(title='Path Finder', message='No path was found.')
	root.quit()
	root.destroy()


def path_found_alert():
	root = tk.Tk()
	root.withdraw()
	tk.messagebox.showinfo(title='Path Finder', message='Path found.')
	root.quit()
	root.destroy()


def restart():
	root = tk.Tk()
	root.withdraw()
	ans = tk.messagebox.askquestion(title='Path Finder', message='Do you want to restart?')
	return ans


if __name__ == '__main__':
	initial_prompt()

	grid_size.val = [i+2 for i in grid_size.val]
	screen = pygame.display.set_mode((grid_size.val[0]*PIXEL_SIZE, grid_size.val[1]*PIXEL_SIZE))
	pygame.display.set_caption('A* Path Finding Algorithm Visualization')

	while True:
		# Initialize grid and screen setup
		screen.fill(BG_COLOR)
		grid = []
		for row in range(grid_size.val[1]):
			grid.append([])
			for col in range(grid_size.val[0]):
				grid[-1].append(pixel(row, col))

		for row in grid:
			for spot in row:
				spot.draw(screen, GREY, 1)

		time.sleep(0.4)
		for spot in grid[0]:
			spot.draw(screen, GREY)
			spot.active = False
		for spot in grid[-1]:
			spot.draw(screen, GREY)
			spot.active = False
		for row in grid:
			row[0].draw(screen, GREY)
			row[0].active = False
			row[-1].draw(screen, GREY)
			row[-1].active = False
		pygame.display.update()

		prompt_start_end()
		grid[start_point.val[0]][start_point.val[1]].active = False
		grid[start_point.val[0]][start_point.val[1]].draw(screen, RED)
		grid[end_point.val[0]][end_point.val[1]].draw(screen, DARK_GREEN)


		# Loop to select obstacles
		draw = True
		while draw:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
						draw = False

				elif pygame.mouse.get_pressed()[0]:
					try:
						pos = pygame.mouse.get_pos()
						mouse_x, mouse_y = pos
						index_x = mouse_x // PIXEL_SIZE
						index_y = mouse_y // PIXEL_SIZE

						if grid[index_x][index_y].active:
							grid[index_x][index_y].active = False
							grid[index_x][index_y].draw(screen, GREY)

					except AttributeError:
						pass


		# Performs a* algorithm
		for row in grid:
			for spot in row:
				spot.h_score = heuristic(spot, grid[end_point.val[0]][end_point.val[1]])
				spot.f_score = spot.g_score + spot.h_score

		completed = []
		future = [grid[start_point.val[0]][start_point.val[1]]]

		search = True
		while len(future) > 0 and search:
			current = future.pop(0)
			neighbors = current.check_neighbors(grid, screen)
			for i,j in neighbors:
				# Break if the end point is reached
				if i==end_point.val[0] and j==end_point.val[1]:
					search = False
					break

				grid[i][j].draw(screen, GREEN)
				if grid[i][j] not in future:
					future.append(grid[i][j])
					time.sleep(0.01)

			# Sorts the pixels that are to be processed by f_score and then h_score if they have same f_score.
			future = sorted(future, key=lambda p:(p.f_score, p.h_score))

			current.draw(screen, RED)

		# Draws path if there is one.
		if search:
			no_path_alert()
		else:
			time.sleep(1)
			path = [grid[end_point.val[0]][end_point.val[1]]]

			while path[-1].previous:
				path.append(path[-1].previous)

			for spot in reversed(path):
				spot.draw(screen, BLUE)
				time.sleep(0.02)
			path_found_alert() 

		# Checks if user wants to restart
		ans = restart()
		if ans != 'yes':
			pygame.quit()
			break


