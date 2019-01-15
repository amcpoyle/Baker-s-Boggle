# started on 12/26/2018
import random
import string
import numpy as np
import csv
import datetime
import re

# with open("words.txt", "r") as f:
# 	words = []
# 	for item in f:
# 		words.append(item)

percent_frequency = {
	'E': 0.1202, 'T': 0.091, 'A': .0812, 'O': 0.0768, 'I': 0.0731, 'N': 0.0695, 'S': 0.0628,
	'R': 0.0602, 'H': 0.0592, 'D': 0.0432, 'L': 0.0398, 'U': 0.0288, 'C': 0.0271, 'M': 0.0261,
	'F': 0.023, 'Y': 0.0211, 'W': 0.0209, 'G': 0.0203, 'P': 0.0182, 'B': 0.0149, 'V': 0.0111,
	'K': 0.0069, 'X': 0.0017, 'Q': 0.0011, 'J': 0.001, 'Z': 0.0007}
	
frequency_per_169 = {}


for letter, freq in zip(percent_frequency.keys(), percent_frequency.values()):
	number_letters = random.randint(0, int(freq * 169))
	if number_letters == 0:
		number_letters = 1
	frequency_per_169[letter] = number_letters # Z and stuff initially came to 0 after int conversion

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
			'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

random_letter_options = []
for letter, number in zip(frequency_per_169.keys(), frequency_per_169.values()):
	# https://stackoverflow.com/questions/3459098/create-list-of-single-item-repeated-n-times-in-python
	options = [letter] * number
	random_letter_options.append(options)

# https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
random_letter_options = [letter for sublist in random_letter_options for letter in sublist]

# random_letters = []
# for i in range(0, 169):
# 	letter = random.choice(random_letter_options)
# 	random_letters.append(letter)



# source: https://stackoverflow.com/questions/49076857/create-arrays-of-random-letters-python-3
# array = np.random.choice(list(string.ascii_lowercase), size=(13, 13))
array = np.random.choice(random_letter_options, size=(13,13))
# random.shuffle(array)


row0 = str(''.join(array[0]))
row1 = str(''.join(array[1]))
row2 = str(''.join(array[2]))
row3 = str(''.join(array[3]))
row4 = str(''.join(array[4]))
row5 = str(''.join(array[5]))
row6 = str(''.join(array[6]))
row7 = str(''.join(array[7]))
row8 = str(''.join(array[8]))
row9 = str(''.join(array[9]))
row10 = str(''.join(array[10]))
row11 = str(''.join(array[11]))
row12 = str(''.join(array[12]))
print(list(row0))
print(list(row1))
print(list(row2))
print(list(row3))
print(list(row4))
print(list(row5))
print(list(row6))
print(list(row7))
print(list(row8))
print(list(row9))
print(list(row10))
print(list(row11))
print(list(row12))
print()


# # source: https://stackoverflow.com/questions/746082/how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-solver

grid = row0 + ' ' + row1 + ' ' + row2 + ' ' + row3 + ' ' + row4 + ' ' + row5 + ' ' + row6 + ' ' + row7 + ' ' + row8 + ' ' + row9 + ' ' + row10 + ' ' + row11 + ' ' + row12

grid = grid.split()
nrows, ncols = len(grid), len(grid[0])
words_path = "D:/Programming/baker's boggle/words.txt"

class TrieNode:

	def __init__(self, parent, value):
		self.parent = parent
		self.children = [None] * 26
		self.isWord = False 
		if parent is not None:
			parent.children[abs(97 - ord(value))] = self


def MakeTrie(dictfile):
	d = open(dictfile)
	root = TrieNode(None, '')
	for word in d:
		curNode = root
		# note: curNode.children is of type 'list'
		# at beginning filled with 26 'None' values
		for letter in word.lower():
			if 97 <= ord(letter) < 123:
				# he did this wrong
				# have to do abs. value 97 to get position to fill
				# ex: 'bar'
				# 97 - 98 = -1 = 1 = where 'b' is supposed to be put
				nextNode = curNode.children[abs(97-ord(letter))]
				if nextNode is None:
					nextNode = TrieNode(curNode, letter)
				curNode = nextNode
		curNode.isWord = True
	return root

def BoggleWords(grid, d):
	rows = len(grid)
	cols = len(grid[0])
	queue = []
	words = []
	for y in range(cols):
		for x in range(rows):
			c = grid[x][y]
			# changed...
			c = c.lower()
			try:
				node = d.children[abs(97-ord(c))]
			except IndexError:
				print(c)
				print(ord(c))
				print()
			if node is not None:
				queue.append((x, y, c, node))

	while queue:
		x, y, s, node = queue[0]
		del queue[0]
		for dx, dy in ((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1,1)):
			x2, y2 = x + dx, y + dy
			if 0 <= x2 < cols and 0 <= y2 < rows:
				y2x2_grid = grid[y2][x2]
				y2x2_grid = y2x2_grid.lower() 
				s2 = s + y2x2_grid
				node2 = node.children[abs(97 - ord(y2x2_grid))]
				if node2 is not None:
					if node2.isWord:
						words.append(s2)
					queue.append((x2, y2, s2, node2))

	words = [word for word in words if len(word) >= 3]
	return words



d = MakeTrie(words_path)
words_returned = BoggleWords(grid, d)
words_returned = list(words_returned)
print(grid)

# for i in range(len(grid)):
# 	row = grid[i]
# 	new_str = str()
# 	for letter in row:
# 		new_str = new_str + str(letter) + ','
# 	print(new_str)
# print()
# print()
# print(grid)

# print()
# print(words_returned)
# np.savetxt("D:/Programming/baker's boggle/boggle problems and solutions/boggle_problem_template1.xltx", grid, delimiter=",")

# with open("D:/Programming/baker's boggle/boggle problems and solutions/updated_boggle_solution.txt", 'w') as f:
# 	for item in words_returned:
# 		f.write("%s\n" % item)
# WORKS