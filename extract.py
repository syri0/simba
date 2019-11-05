import requests
import re
from bs4 import BeautifulSoup

def casemaker(msg):
    return msg.lower()

def wikisp(msg):
    typo=0
    if ("what is the" in msg ):
        typo=1
        msg=msg.replace("what is ","")
    elif("what's the" in msg):
        typo=2
        msg= msg.replace("what's ","")
    elif("who's" in msg):
        typo=3
        msg= msg.replace("who's ","")
    elif("who is" in msg):
        typo=4
        msg= msg.replace("who is ","")  

    msg=msg.replace("?","")
    msg= msg.strip()
    msg= " ".join(msg.split())
    words = msg.split(' ')
    whitelist = {'and', 'the', 'is', 'of'}
    capitalized = ' '.join([word.title() if word not in whitelist else word for word in words])
    capitalized=capitalized.replace(" ","_")
    print "link of capitalized"
    print capitalized
    wiki_url= "https://en.wikipedia.org/wiki/"+capitalized
    resp= requests.get(wiki_url)
    soup = BeautifulSoup(resp.content)
    blocks= soup.findAll('p')
    result=""
    for block in blocks:
    	if ("Narendra" in str(block) and "Modi" in str(block)):
    		print (str(block))
    #print str(blocks)
    for block in blocks:
    	#lower=casemaker(block)
    	blk=str(block)
    	print block
    	print blk
    	flag=1
    	for word in words:
    		w=word.title()
    		if w not in blk:
    			print "\n\n"
    			print w
    			print "|||||Here||||||"
    			print blk
    			print "\n\n"
    			flag=0
    	if (flag==1):
    		result=blk
    		break
    print "Result is:"+str(result)




def wiki(msg):
    typo=0
    if ("what is the" in msg ):
        typo=1
        msg=msg.replace("what is ","")
    elif("what's the" in msg):
        typo=2
        msg= msg.replace("what's ","")
    elif("who's" in msg):
        typo=3
        msg= msg.replace("who's ","")
    elif("who is" in msg):
        typo=4
        msg= msg.replace("who is ","")  

    msg=msg.replace("?","")
    msg= msg.strip()
    msg= " ".join(msg.split())
    words = msg.split(' ')
    whitelist = {'and', 'the', 'is', 'of'}
    capitalized = ' '.join([word.title() if word not in whitelist else word for word in words])
    capitalized=capitalized.replace(" ","_")
    print "link of capitalized"
    print capitalized
    wiki_url= "https://en.wikipedia.org/wiki/"+capitalized
    resp= requests.get(wiki_url)
    content= str(resp.content)
    print content
    blocks = re.findall(r'<p>(.*?)?</p>', content)
    result=""
    print blocks
    for block in blocks:
    	block=casemaker(str(block))
    	f=1
    	for w in words:
    		print "w is:"+str(w)
    		print "block is:"+str(block)
    		if w!=block:
    			f=0
    	if f==1:
    		result=block
    print "result is: "
    print result
    return result



#msg= raw_input("msg:")
print wikisp(casemaker("narendra modi"))