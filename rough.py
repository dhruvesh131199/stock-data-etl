s = "paypalishiring"
numOfRow = int(input("numOfRow: "))

completeCol = 0
sLen = len(s)
numOfCol = 0

while sLen > 0:

	if completeCol == 0:
		numOfCol += 1
		completeCol = numOfRow - 2
		sLen -= numOfRow
	else:
		numOfCol += 1
		sLen -= 1
		completeCol -= 1

grid = [[""]*numOfCol for _ in range(numOfRow)]

sIndex = 0
completeCol = 0

for i in range(numOfCol):

	if sIndex == len(s) - 1:
		break
	if completeCol == 0:
		for j in range(numOfRow):
			if sIndex == len(s) - 1:
				break
			grid[j][i] = s[sIndex]
			sIndex += 1
		completeCol = numOfRow - 2
	else:
		grid[completeCol][i] = s[sIndex]
		completeCol -= 1
		sIndex += 1

for i in range(numOfRow):
	print(grid[i][:])
