#encoding: utf-8
import numpy as np
import sys
import pygame
from pygame.locals import *
from n_queens_solver import n_queens_solver
from ChessGUI_pygame import ChessGUI_pygame
 
def get_solutions_and_build_animation(InitialBoard):
	#Get configurations and build animation (solving 8 queens problem)
	solver = n_queens_solver(board_size=8)
	configs = list(solver.get_solutions()) #get_solutions() return a 3D tensor of shape [n_solutions,board_size,board_size]
	configs.insert(0,InitialBoard) #add initial board config to the configs set at the beginning
	configs.append(InitialBoard) #add initial board config to the configs set at the end   
	animation = [] 
	#A configuration is a matrix of 2 char strings: "wQ" means queen and "ee" means empty.
	cases = dict(eeee="ee",eewQ="X",wQee="wQ",wQwQ="wQ") #the concatenation gives 4 possible outcomes as shown below
	for k in range(len(configs)-1): 
		config_tmp = np.char.add(configs[k],configs[k+1]) #element-wise string concatenation for two arrays of str or unicode
		config_tmp = np.vectorize(cases.get)(config_tmp) #translate every element in numpy array according to key
		animation.append(configs[k])
		animation.append(config_tmp)
	return np.array(animation) #return a 3D tensor of shape [animation_size,board_size,board_size]

if __name__ == "__main__":
	#Define initial configuration 
	InitialBoard = np.array([["ee"]*8]*8)
	InitialBoard[0,:] = 'wQ'

	#build animation 
	animation = get_solutions_and_build_animation(InitialBoard)
	print("1 mouse click --> pieces make 1 movement")
	print("Use the escape or Q keys to end program")

	#drawing board
	Gui = ChessGUI_pygame(1)
	Gui.PrintMessage("Stand by..."), Gui.PrintMessage("   ")
	Gui.Draw(InitialBoard)

	#control variables
	k = 1 #configuration counter  
	highlight = True #helps for highlighting queen's future movements during animation 

	#Start GUI stuff
	pygame.event.set_blocked(MOUSEMOTION)
	while True:
		e = pygame.event.wait()
		#Quit animation closing the window
		if e.type == QUIT:
			pygame.quit()
			sys.exit()
		#Quit pressing escape or key q
		if e.type == KEYDOWN:
			if e.key == K_ESCAPE or e.key == K_q:
				pygame.quit()
				sys.exit()
		#Pressing a mouse button fires an event
		if e.type == MOUSEBUTTONDOWN:
			if k<(len(animation)-1):
				if not highlight:
					Gui.PrintMessage("Arrangement Id:  "+str(int(k/2)))
					Gui.PrintMessage("   "), Gui.Draw(animation[k])
					highlight = True
				else:
					Gui.PrintMessage("Next move highlighted"), Gui.PrintMessage("   ")
					Gui.Draw(animation[k])
					highlight = False
				k += 1
			elif k>=(len(animation)-1): 
				if not highlight:
					k = 1 #reset animation
					Gui.PrintMessage("Stand by..."), Gui.PrintMessage("   ")
					Gui.Draw(animation[0])
					highlight = True
				else:
					Gui.PrintMessage("No more arrangements left, next move will reset board"), Gui.PrintMessage("   ")
					Gui.Draw(animation[-1])
					highlight = False
