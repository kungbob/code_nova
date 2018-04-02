import sys

def printStr(x):
	if x >= 0:
		print ('*', end = "")
		printStr(x - 1)

n = int(input())
for i in range(n):
	printStr(i);
	print()
