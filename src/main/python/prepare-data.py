import os
import http.client
import time, datetime
from threading import Thread
from base64 import b64encode

# This is a python script to add XML content to the 'text/plain' enron email files

def process_file(filepath):	
	# open file to read (to filehandle)
	fh = open(filepath, 'r')
	# break lines into large string[] array 
	lines = fh.readlines()
	# rewind to get the entire file for prepending XML
	fh.seek(0)
	original_file = fh.read()
			
	# create metadata XML block
	# init stringbuffer for XML
	sb = []
	sb.append(']]></FullText>')		
	sb.append('<Metadata>')
	sb.append('<FilePath>'+filepath+'</FilePath>')
	for line in lines:
		if line.startswith("Date: "):			
			tdate = line[6:(line.index("(") - 1)]
			sb.append('<DateTime>'+
			datetime.datetime.fromtimestamp(time.mktime(time.strptime(tdate, "%a, %d %b %Y %H:%M:%S %z"))).isoformat()
			+'</DateTime>')
		if line.startswith("From: "):
			sb.append('<From>'+line[6:].strip()+'</From>')
		if line.startswith("To: "):
			sb.append('<To>'+line[4:].strip()+'</To>')
		if line.startswith("Subject: "):
			sb.append('<Subject>'+line[9:].strip()+'</Subject>')
	sb.append('</Metadata></Item>')
	fh.close()
	
	# prepend file with xml opening elements (<Item><FullText>)
	with open(filepath+".xml", "w") as fhw:
		fhw.write('<?xml version="1.0" encoding="UTF-8"?><Item><FullText><![CDATA[' + original_file) 
	
	
	# open file in append mode and add the metadata
	with open(filepath+".xml", "a") as fhw:
		fhw.write("\n".join(sb))
				
	# put data
	print('processing: ' + filepath+".xml")
	connection = http.client.HTTPConnection("localhost", 8003)
	userAndPass = b64encode(b"q:q").decode("ascii")
	headers = { 'Authorization' : 'Basic %s' %  userAndPass, 'Content-type' : 'application/xml' }
	connection.request('PUT', '/v1/documents?uri='+filepath.replace("\\", "/")+'.xml', open(filepath+".xml", 'rb'), headers)
	
	response = connection.getresponse()
	print(str(response.status) + " | " + response.reason + " | "  + response.read().decode())


# traverse the directory from root with os.walk(".")	
# note - relative to cmd if you do the above
for root, dirs, files in os.walk("d:\\test-data\\allen-p\\deleted_items"):
	# print the file and path with :: print (item) 
	for file in files:
	
		# build path to file on filesystem
		t = Thread(target=process_file, args=(os.path.join(root, file),))
		t.start()
		
