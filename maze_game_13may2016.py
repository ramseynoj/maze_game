import sys
import itertools
from itertools import product

inFile = sys.argv[1]
outFile = sys.argv[2]

with open(inFile, 'r') as f:
        lines = f.readlines()

#check input file length
if len(lines) <=1:
	print 'Input file must be 2 lines at minimum'
	sys.exit()

#get starting coordinates
start = lines[1].split()
start_x = int(start[0])
start_y = int(start[1])
initial_coordinate = [start_x, start_y]


mirrors = lines[2:]
mirrors_list = []


for items in mirrors:
        mirrors_list.append(items.split())

#get direction of mirrors
mirrors_direction = []
for items in mirrors_list:
        mirrors_direction.append(items[2])

#get mirror coordinates
mirror_coordinates = []
for items in mirrors_list:
        mirror_coordinates.append([int(items[0]), int(items[1])])

#get grid coordinates
grids = [int(x) for x in (lines[0].split())]
x = int(lines[0].split()[0])
y = int(lines[0].split()[1])

#test grid size
if x<1 or x>1000 or y<1 or y>1000:
	print 'Invalid grid size'
	sys.exit()

#make grid
coordinates = []
for a in range(x):
  for b in range(y):
    coordinates.append((a+1, b+1))

#get min and max grid coordintes
list_coordinates = [list(elem) for elem in coordinates]
max_x = max(list_coordinates)[0]
max_y = max(list_coordinates)[1]
min_x = min(list_coordinates)[0]
min_y = min(list_coordinates)[1]

#get stariting coordinate
moves = []
moves.append(initial_coordinate)

#check input file for duplicates
full_list = [initial_coordinate] + mirror_coordinates
full_list.sort()
full_list_check = list(full_list for full_list,_ in itertools.groupby(full_list))

if len(full_list) != len(full_list_check):
	print 'duplicate values in file'
	sys.exit()

#check if out of bounds
def check_boundaries(x, y, moves):
	if x > 0 and x <= max_x and y > 0 and y <= max_y:
		with open(outFile,'w') as o:
			o.write('Moves on grid: %s' %moves)
		return True
	else:
		with open(outFile,'w') as o:
			del moves[-1]
        		o.write('%s\n%s' %(len(moves), moves[-1]))
			
#traverse maze
def traverse_maze():
	i=0
	while check_boundaries(moves[-1][0], moves[-1][1], moves) == True:
		print i, moves, 'move check'
		if moves[-1] in mirror_coordinates:
			try:
				mirrors_direction[i] == '/'
			except IndexError:
				with open(outFile,'w') as o:
					o.write('-1')
					sys.exit()
			if mirrors_direction[i] == '/':
				i+=1
				#if x1 < x2
				if moves[-1][0] < moves[-2][0]:
					moves.append([moves[-1][0], moves[-1][1]+1])
				#if y1 < y2
				elif moves[-1][1] < moves[-2][1]:
					moves.append([moves[-1][0]+1, moves[-1][1]])
				#if x1 > x2
				elif moves[-1][0] > moves[-2][0]:
					moves.append([moves[-1][0], moves[-1][1]-1])
				#if y1 > y2
				elif moves[-1][1] > moves[-2][1]:
					moves.append([moves[-1][0]-1, moves[-1][1]])
			elif mirrors_direction[i] == '\\':
				i+=1
				#if x1 < x2
				if moves[-1][0] < moves[-2][0]:
					moves.append([moves[-1][0], moves[-1][1]-1])
				#if y1 < y2
				elif moves[-1][1] < moves[-2][1]:
					moves.append([moves[-1][0]-1, moves[-1][1]])
				#if x1 > x2
				elif moves[-1][0] > moves[-2][0]:
					moves.append([moves[-1][0], moves[-1][1]+1])
				#if y1 > y2
				elif moves[-1][1] > moves[-2][1]:
					moves.append([moves[-1][0]+1, moves[-1][1]])
		elif moves[-1] not in mirror_coordinates:
			#if x1 < x2
			if moves[-1][0] < moves[-2][0]:
				moves.append([moves[-1][0]-1, moves[-1][1]])
			#if y1 < y2
			if moves[-1][1] < moves[-2][1]:
				moves.append([moves[-1][0], moves[-1][1]-1])
			#if x1 > x2
			if moves[-1][0] > moves[-2][0]:
				moves.append([moves[-1][0]+1, moves[-1][1]])
			#if y1 > y2
			if moves[-1][1] > moves[-2][1]:
				moves.append([moves[-1][0], moves[-1][1]+1])

#set initial movement of laser and begin maze
if 'S' in start:
        moves.append([moves[0][0], moves[0][1]+1])
        traverse_maze()
if 'N' in start:
	moves.append([moves[0][0], moves[0][1]-1])
	traverse_maze()
if 'E' in start:
	moves.append([moves[0][0]+1, moves[0][1]])
	traverse_maze()
if 'W' in start:
	moves.append([moves[0][0]-1, moves[0][1]])
	traverse_maze()
