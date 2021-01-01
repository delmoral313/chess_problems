# Created by Oscar Del Moral 
#18/Nov/2018
#encoding: utf-8
import sys
import numpy as np

class n_queens_solver(object):
    def __init__(self,board_size):
        self.N = board_size #chess board size 
        self.solutions = [] #solution set
        self.T = np.array([["ee"]*self.N]*self.N) #init chess board
        self.k = 0 #solutions counter, that is to say, the number of configurations that are solutions 
        self.find_solutions_status = False #the find_solutions has not been executed  

    def there_is_attack(self,row,column):
        '''checking if there is a queen on some column from [0,column-1] of the given row. 
        If so, True is returned.'''
        for j in range(column):
            if self.T[row,j] == 'wQ': #"wQ" stands for white queen
                return True 
        '''checking if there is a queen on the top diagonal that is on the left stood at T[row,column].
        If so, True is returned. The top diagonal that is on the right isn't checked since there's nothing
        (since the queens are placed from left to right).'''
        x = row
        y = column
        while (x>=0 and y>=0):
            if self.T[x,y] == 'wQ':
                return True
            x -= 1
            y -= 1
        '''checking if there is a queen on the botton diagonal that is on the left stood at T[row,column].
        If so, True is returned.'''         
        x = row
        y = column
        while (x<self.N and y>=0):
            if (self.T[x,y] == 'wQ'):
                return True
            x += 1
            y -= 1          
        return False

    def find_solutions(self,column):
        self.find_solutions_status = True #change status to notify that this method has been executed
        '''If all queens were successfully placed, then...'''
        if column == self.N:
            self.k += 1 #new solution found 
            self.solutions.append(self.T.copy()) #save configuration 
            return True #this statement will stop recursion  
        '''If not, then...'''
        for i in range(self.N): #for all rows 
            #if there is not threat at position T[i,colum], then...
            if not self.there_is_attack(row=i,column=column):
                self.T[i,column] = 'wQ' #place a queen on such position 
                '''checking if a queen can be placed on some row of the next column (recursive step)'''
                self.find_solutions(column=column+1)
                #backtracking: remove the queen just placed and explore for the next row. 
                self.T[i,column] = 'ee' # "ee" stands for empty 

    def get_solutions(self):
        #find solutions and return them
        if self.find_solutions_status == False:
            self.find_solutions(column=0)
            print("Number of solutions: "+str(self.k))
        return self.solutions #return a 3D tensor of shape [n_solutions,board_size,board_size]
