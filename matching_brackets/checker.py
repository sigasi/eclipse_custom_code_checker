#!/usr/bin/python

def readFile(filename):
	f=file(filename)
	lines=f.readlines()
	f.close()
	return lines

def stripComments (line, commentSymbol='--'):
	pos = line.find(commentSymbol)
	if pos != -1:
		result = (pos + len(commentSymbol))*" " + line[pos + len(commentSymbol):]
	else:
		result = " "* len(line)
	if line and line[-1]=='\n':
		result = result[:-1] + line[-1]
	return result

def reportError(report,filename,lineNumber, charStart=-1,charEnd=-1, message = "Warning"):
	if charStart!=-1:
		reportLine = "%s\t%d\t%d\t%d\t%s\n"%(filename,lineNumber+1,charStart,charEnd,message)
	else:
		reportLine = "%s\t%d\t%s\n"%(filename,lineNumber+1, message)
	report += reportLine

def checkMatchingBrackets(report,filename,lines):
	content = "".join(lines)
	brackets={
			'[':']',
			'(':')',
			'{':'}',
			}
	pos = 0
	stack = []
	for char in content:
		if char in brackets.keys():
			stack.append( (char,pos) )
		if char in brackets.values():
			if not stack:
				reportError(report,filename,0,pos,pos+1, "Unexpected closing bracket '%s'"%char)
			elif stack and brackets[stack[-1][0]] == char:
				stack.pop()
			else:
				reportError(report,filename,0,pos,pos+1 ,"Bracket does not match '%s'"%(stack[-1][0]))
		pos +=1
	for stackItem in stack:
		reportError (report,filename,0,stackItem[1],stackItem[1]+1, "Bracket is not closed: "+stackItem[0])

def writeReport(report):
	f=file('markers.rpt','w')
	f.writelines(report)
	f.close()

def checkFile(report,filename):
	lines = readFile(filename)
	lines = [stripComments(line) for line in lines]
	checkMatchingBrackets(report,filename,lines)

def findVHDLfiles():
	import fnmatch
	import os
	
	matches = []
	for root, dirnames, filenames in os.walk('.'):
		for filename in fnmatch.filter(filenames, '*.vhd'):
			matches.append(os.path.join(root, filename))
	return matches

def main():
	report = []
	for fileName in findVHDLfiles():
		checkFile(report,fileName)
	writeReport(report)

main()