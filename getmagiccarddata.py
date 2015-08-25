#
# Created:     26/02/2012
# Copyright:   (c) Geoff 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import urllib.request, urllib.parse, urllib.error
import re
import os
import codecs


//Thinking about renaming the file to be the name of the card (cardinfo[1]) rather than the number of the card - but then that might mess up indexing on a db level.
if(os.uname().sysname == "Darwin"):
    path = "/Users/peter/Documents/Projects/MTG/Images/"
    dirDelim = "/"
else:
    path = "E:\\Magic Card Images\\"
    dirDelim = "\\"

for root, dirs, files in os.walk(path):
    if len(dirs) > 0:
        for dir in dirs:
            data = urllib.request.urlopen("http://magiccards.info/"+dir+"/en.html")
            lines = data.read().decode('utf-8').split('\n')
            state = 0
            cardinfo = []
            for line in lines:
                if state == 4:
                    featureFile = path + dir + dirDelim + cardinfo[0] + ".txt"
                    file = codecs.open(featureFile, 'w', 'utf-8')
                    for item in cardinfo:
                        file.write(item + '\n')
                    print(cardinfo)
                    print(featureFile)
                    cardinfo = []
                    state = 0
                elif state != 0:
                    line = line.lstrip().rstrip()
                    line = line.lstrip("<td")
                    line = line.lstrip(">")
                    line = line.rstrip("/td>")
                    line = line.rstrip("<")
                    line = cardinfo.append(line)
                    state = state + 1
                else:
                    it = re.finditer(re.escape("<a href=\"/") + dir + re.escape("/en/") + "(\d*\w*)" + re.escape(".html\">") + "([^<]*)", line)
                    try:
                        value = next(it)
                    except StopIteration:
                        continue
                    cardnumber = value.group(1)
                    cardname = value.group(2)
                    cardinfo.append(cardnumber)
                    cardinfo.append(cardname)
                    state = 1


