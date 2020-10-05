#Author: Kyle Wilson
#Init: 5/30/2018
#Last Updated: 5/30/2018
#Purpose: Read from a specified text format and produce a formatted html file from that information.

from random import randint

#Per block: [bg_color, font_color]
blockStyles = (["#06406c", "#FFF"], ["#FFF", "#000"], ["#4c0d09", "#d3b2af"], 
	["cc4037", "#4c0d09"], ["#000", "#FFF"], ["#fff8c9", "#2d2700"])

def count_indents(_s):
	for i in range(0, len(_s) - 1):
		if not (_s[i] == '\t'):
			return i - 1
	return None

#read from text file
with open("./notes.txt") as f:
    content = f.readlines()
content = [x.replace('\n', '') for x in content]

numBlocks = 0
biggestIndent = 0

#begin populating html
html = []
html.append("<!DOCTYPE html>")
html.append("<html lang='en'>")
html.append("<head>")
html.append("<link href='http://fonts.googleapis.com/css?family=Chelsea+Market' rel='stylesheet' type='text/css'>")
html.append("<meta charset='utf-8'>")
html.append("<title>" + content[0] + "</title>")

#write static css
html.append("<style type='text/css'>")
html.append(".title {")
html.append("font-size: 80px;")
html.append("font-weight: bold;")
html.append("font-family: 'Chelsea Market', Georgia, serif;")
html.append("text-align: center;")
html.append("}")

html.append(".subtitle {")
html.append("font-size: 60px;")
html.append("font-weight: bold;")
html.append("font-family: 'Chelsea Market', Georgia, serif;")
html.append("text-align: center;")
html.append("}")

html.append(".head {")
html.append("font-size: 70px;")
html.append("font-weight: normal;")
html.append("font-family: 'Chelsea Market', Georgia, serif;")
html.append("text-align: center;")
html.append("}")

html.append("li {")
html.append("margin: 1em 0;")
html.append("}")


html.append(".detail {")
html.append("font-family: Georgia, Times New Roman, Times, serif;")
html.append("font-size: 30px;")
html.append("}")

html.append(".sub_detail {")
html.append("font-family: Georgia, Times New Roman, Times, serif;")
html.append("font-size: 24px;")
html.append("}")

html.append(".block {")
html.append("width: 100%;")
html.append("}")

html.append(".block_inner {")
html.append("padding-top: 80px;")
html.append("padding-bottom: 80px;")
html.append("width: 80%;")
html.append("margin: 0 auto;")
html.append("}")

html.append("</style>")

#close head and add body
html.append("</head>")
html.append("<body>")

#create title block
numBlocks += 1
html.append("<div class='block title_block'>")
html.append("<div class='block_inner title_block_inner'>")
for i in range(len(content)):
	#if you find a blank line, end the title block and go to the next line
	if content[i] == '':
		i += 1
		break
	else:
		if i == 0:
			html.append("<p class='title'>" + content[i] + "</p>")
		else:
			html.append("<p class='subtitle'>" + content[i] + "</p>")

#create blocks
for j in range(i, len(content)):
	#if the current line is not indented, start a new block
	if content[j][:1] != "\t":
		html.append("</div>")
		html.append("</div>")

		numBlocks += 1

		html.append("<div class='block block_" + str(numBlocks) + "'>")
		html.append("<div class='block_inner block_" + str(numBlocks) + "_inner'>")

		html.append("<p class='head'>" + content[j] + "</p>")

	else:
		#count indents
		if count_indents(content[j]) == 0:			
			html.append("<p class='detail'>" + content[j].strip() + "</p>")
		else:
			html.append("<li class='sub_detail sub_detail_" + str(count_indents(content[j])) + "'>" + content[j].strip() + "</li>")
			#check for biggest indent
			if biggestIndent < count_indents(content[j]):
				biggestIndent = count_indents(content[j])

#end last block
html.append("</div>")
html.append("</div>")

#end html
html.append("</body>")
html.append("</html>")

#insert dynamic css
css = []

#block styling
lastStyle = None
styleNum = randint(0, len(blockStyles)-1)
for a in range(numBlocks-1): #not styling title block
	#randomly pick a style that is not the most previoulsy used style
	while styleNum == lastStyle:
		styleNum = randint(0, len(blockStyles)-1)
	lastStyle = styleNum

	css.append(".block_" + str(a+2) + " {")
	css.append("background-color: " + blockStyles[styleNum][0] + ";")
	css.append("}")

	css.append(".block_" + str(a+2) + "_inner p, .block_" + str(a+2) + "_inner li {")
	css.append("color: " + blockStyles[styleNum][1] + ";")
	css.append("}")

for b in range(biggestIndent):
	css.append(".sub_detail_" + str(b+1) + " {")
	css.append("text-indent: " + str((b+1)*30) + "px;")
	css.append("}")

html[html.index("</style>"):html.index("</style>")] = css

#write file
f = open("./webified.html", 'w')
[f.write(x + "\n") for x in html]		
f.close()
