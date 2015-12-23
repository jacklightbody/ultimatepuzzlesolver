import sys
class Piece:
	'''
	Key for edges
	listed clockwise from top to left
	1 for the circle
	2 for the inward pointing arrow
	3 for the outward pointing arrow
	4 for the cross 

	Key for possible rotations
	0 with male edges top and right 
	1 with male edges right and bottom (90 degree roation)
	2 with male edges bottom and left (180 degree rotation)
	3 with male edges left and top (270 degree rotation)
	'''
	def __init__(self, edges):
		self.edges = edges
		self.rotation = 0
		self.sideDict = {
		'top': 0,
		'right': 1,
		'bottom': 2,
		'left': 3,
	}

	def rotate(self,rotation):
		self.rotation = rotation
	def getRotation(self):
		return self.rotation

	def getEdge(self,side):
		base = self.sideDict[side]
		return self.edges[((base+self.rotation)%4)]

	def getName(self):
		return ''.join([str(i) for i in self.edges])

class Puzzle:
	def __init__(self):
		self.width = 4
		self.height = 4
		self.board = []
		self.solutions = []
		self.pieces = []
		self.count = 0
		self.solutionNames = []
		self.createBoard()
		pieces = [
			[1,1,-1,-3],
			[1,2,-1,-4],
			[1,2,-2,-3],
			[1,2,-4,-2],
			[1,4,-2,-1],
			[1,4,-3,-3],
			[1,4,-4,-1],
			[2,2,-1,-4],
			[2,2,-3,-4],
			[2,3,-3,-1],
			[2,4,-3,-2],
			[3,1,-1,-3],
			[3,1,-1,-4],
			[3,3,-1,-2],
			[4,3,-3,-1],
			[4,3,-4,-2]]
		for pieceEdges in pieces:
			self.pieces.append(Piece(pieceEdges))
		self.solveInit()

	def createBoard(self):
		self.board = [None]*self.height
		for i in range(0,self.height):
			# add a row of self.width units 
			# self.height times
			# should always be 4/4, but for flexibility sake
			self.board[i] = [None] * self.width

	def isUsed(self,piece, board, used):
		return piece.getName() in used

	def solve(self,xloc,yloc,board,used):
		if(xloc == self.width):
			xloc = 0
			yloc = yloc+1
		if(yloc == self.height):
			self.solution(board,used)
			return True

		for piece in self.pieces:
			if self.isUsed(piece,board,used):
				continue
			for i in range(0,4):
				piece.rotate(i)
				if yloc == 0 or board[yloc-1][xloc].getEdge('bottom') + piece.getEdge('top') == 0:
					if xloc == 0 or board[yloc][xloc-1].getEdge('right') + piece.getEdge('left') == 0:
						board[yloc][xloc] = piece
						newused = used[:]
						newused.append(piece.getName())
						self.solve(xloc+1,yloc,board,newused)
		return False

	def solution(self, board,used):
		if board not in self.solutions:
			self.count += 1
			print self.count
			self.prettyPrint(board)
			self.solutions.append(board)

	def showSolutions(self):
		for solution in self.solutions:
			self.prettyPrint(solution)

	def prettyPrint(self,board):
		for i in range(0,self.height): 
			r = ''
			for k in range(0,self.width): 
				r = r + board[i][k].getName()+"r"+str(board[i][k].getRotation())+"   "
			print r
		print ''
	def solveInit(self):
		'''
		We're going to solve from the top left to the right
		always going down and right
		so the important slots to check are the top and left slots
		'''
		yloc = 0
		xloc = 0
		board = self.board
		for piece in self.pieces:
			for i in range(0,4):
				piece.rotate(i)
				board[yloc][xloc] = piece
				self.solve(xloc+1,yloc,board,[piece.getName()])

def main():
	Puzzle()

if __name__ == "__main__":
        main()
