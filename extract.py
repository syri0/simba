import requests
import re
from bs4 import BeautifulSoup
import time
def casemaker(msg):
    return msg.lower()


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def getwikifilter(wiki_uri):
    resp= requests.get(wiki_url)
    soup = BeautifulSoup(resp.content)
    blocks= soup.findAll('p')
    result=""
    for block in blocks:
        if(len(cleanhtml(str(block)))>100):
            result= (cleanhtml(str(block)))
            break
    return result

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
    result=getwikifilter(wiki_uri)
    return result

def autocomplete(msg):
    retvar={}
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
    msg=msg.replace(" ","+")

    url="https://www.google.com/search?q="+str(msg)
    resp= requests.get(url)
    cont= str(resp.content)
    wikiuri=""
    try:
        an= re.search(r"{var q='(.*?)?';", str(cont)).group(1)
        retvar["corrected"]=an
    except:
        retvar["corrected"]=msg
    try:
        wiki= re.findall(r'<div class="kCrYT"><a href="(.*?)?"><div class="BNeawe vvjwJb AP7Wnd', cont)
        for wik in wiki:
            #print wik
            #print "\n-------------\n"
            if("en.wikipedia" in wik):
                wikiuri= wik
                wikiuri=wikiuri.replace("/url?q=","")
                #break
        retvar["wikiuri"]=wikiuri.split("&")[0]
    except:
         retvar["wikiuri"]=""
    return retvar
    #print an
   # print  wiki

    #print str(blocks)
    # for block in blocks:
    # 	#lower=casemaker(block)
    # 	blk=str(block)
    # 	print block
    # 	print blk
    # 	flag=1
    # 	for word in words:
    # 		w=word.title()
    # 		if w not in blk:
    # 			print "\n\n"
    # 			print w
    # 			print "|||||Here||||||"
    # 			print blk
    # 			print "\n\n"
    # 			flag=0
    # 	if (flag==1):
    # 		result=blk
    # 		break
    #print "Result is:"+str(result)




# def wiki(msg):
#     typo=0
#     if ("what is the" in msg ):
#         typo=1
#         msg=msg.replace("what is ","")
#     elif("what's the" in msg):
#         typo=2
#         msg= msg.replace("what's ","")
#     elif("who's" in msg):
#         typo=3
#         msg= msg.replace("who's ","")
#     elif("who is" in msg):
#         typo=4
#         msg= msg.replace("who is ","")  

#     msg=msg.replace("?","")
#     msg= msg.strip()
#     msg= " ".join(msg.split())
#     words = msg.split(' ')
#     whitelist = {'and', 'the', 'is', 'of'}
#     capitalized = ' '.join([word.title() if word not in whitelist else word for word in words])
#     capitalized=capitalized.replace(" ","_")
#     print "link of capitalized"
#     print capitalized
#     wiki_url= "https://en.wikipedia.org/wiki/"+capitalized
#     resp= requests.get(wiki_url)
#     content= str(resp.content)
#     print content
#     blocks = re.findall(r'<p>(.*?)?</p>', content)
#     result=""
#     print blocks
#     for block in blocks:
#     	block=casemaker(str(block))
#     	f=1
#     	for w in words:
#     		print "w is:"+str(w)
#     		print "block is:"+str(block)
#     		if w!=block:
#     			f=0
#     	if f==1:
#     		result=block
#     print "result is: "
#     print result
#     return result



# msg= raw_input("msg:")
# print wikisp(casemaker(msg))
ok= autocomplete("mithila")



print ok["corrected"]
print ok["wikiuri"]