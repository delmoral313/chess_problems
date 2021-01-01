#encoding: utf-8 
import numpy as np
import sys
import pygame
from Warnsdorff_Heuristic import Warnsdorff_Heuristic
from pygame.locals import *
from ChessGUI_pygame import ChessGUI_pygame
from ChessBoard import ChessBoard

def build_animation(T):
	N = len(T) # board size
	depth = N**2 #number of board configurations 
	height = N #number of board rows
	width = N #number of board columns 

	animation = np.array([[["eee"]*height]*width]*depth) #3D tensor of strings (3 characters) 
	positions = np.empty(depth,dtype=object) #1D tensor of coordinates (represented as tuples)
	for k in range(depth):
		for i in range(height):
			for j in range(width):
				if T[i,j] == k: #place knight for kth config 
					animation[k,i,j] = "wT" #"wT" will make the GUI to place the knight at position (i,j) for the kth board configuration
					positions[k] = (i,j) #save knight position for the kth configuration 
				if k>0:
					#draw the kth config
					if T[i,j]<k and (animation[k-1,i,j]=="wT" or animation[k-1,i,j]=="X" or animation[k-1,i,j]=="Xo"):
						if T[i,j] != 0:
							animation[k,i,j] = "X" #"X" means that the (i,j) box for the kth config has been visited
						else:
							animation[k,i,j] = "Xo" #"Xo" marks the origin (position where the tour started)
	return animation,positions

def get_animation_set():
    tour = Warnsdorff_Heuristic(board_size=8)
    T = tour.build() #T is a NxN matrix encoding the tour  
    print("Knight's Tour..." )
    print("Tour found after %d trials" % (tour.trials))
    animation,positions = build_animation(T)
    return animation,positions

if __name__ == "__main__":
	#solving the knight's tour problem 
	animation,positions = get_animation_set()
	print("1 mouse click --> pieces make 1 movement")
	print("Use the escape or Q keys to end program")
	
	#drawing board
	InitialBoard = animation[0] #initial configuration  
	Board = ChessBoard(0)
	Gui = ChessGUI_pygame(1)
	Gui.PrintMessage("Knight's Tour..."), Gui.PrintMessage("Stand by.."), Gui.PrintMessage("   ")
	Gui.Draw(InitialBoard)

	k = 1 #kth configuration 
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
			if k<len(animation): #if the kth config is valid, then... 
				if k==0: #if initial configuration 
					Gui.PrintMessage("Knight's Tour..."), Gui.PrintMessage("Stand by.."), Gui.PrintMessage("   ")
					Gui.Draw(InitialBoard)
					k += 1
				else:
					Gui.PrintMessage("Move Id:  "+ str(k))
					#Get move from (x,y) to (nx,ny)
					x,y = positions[k-1] 
					nx,ny = positions[k]
					# Get report move
					moveReport = Board.MovePiece(x,y,nx,ny)
					Gui.PrintMessage(moveReport)
					# Draw current Board (configuration)
					Gui.PrintMessage("   ")
					Gui.Draw(animation[k])
					k += 1 #move to the next config 
			elif k >= len(animation): #if no more configurations left, then restart animation  
				Gui.PrintMessage("Tour end")
				# Get move
				x,y = positions[len(animation)-1]
				nx,ny= positions[0]
				# Get report move
				moveReport = Board.MovePiece(x,y,nx,ny)
				Gui.PrintMessage(moveReport), Gui.PrintMessage("   ")
				Gui.Draw(InitialBoard)
				k = 0 #restart animation


