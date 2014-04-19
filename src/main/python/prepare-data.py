import os
import http.client
import time, datetime
import concurrent.futures
from base64 import b64encode

# This will add XML content to the 'text/plain' enron email files and send them over to MarkLogic via an HTTP 'PUT' request

def process_file(filepath):
	xmldoc = filepath + '.xml'
	print('processing: ' + xmldoc)
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
	with open(xmldoc, "w") as fhw:
		fhw.write('<?xml version="1.0" encoding="UTF-8"?><Item><FullText><![CDATA[' + original_file) 
	
	
	# open file in append mode and add the metadata
	with open(xmldoc, "a") as fhw:
		fhw.write("\n".join(sb))

	# put data
	http_put_file(xmldoc)
		

def http_put_file(filename):
	connection = http.client.HTTPConnection("localhost", 8003)
	userAndPass = b64encode(b"q:q").decode("ascii")
	headers = { 'Authorization' : 'Basic %s' %  userAndPass, 'Content-type' : 'application/xml' }
	connection.request('PUT', '/v1/documents?uri='+filename.replace("\\", "/"), open(filename, 'rb'), headers)
	response = connection.getresponse()
	print(str(response.status) + " | " + response.reason + " | "  + response.read().decode())

	
# initialise a Thread Pool (64 worker threads) for concurrent operations
executor = concurrent.futures.ThreadPoolExecutor(max_workers=64)

# traverse the directory from a given root with os.walk(".")	
for root, dirs, files in os.walk("d:\\test-data"):
	# print the file and path with :: print (item) 
	for file in files:
                # task a single thread with the processing for that file
                executor.submit(process_file, os.path.join(root, file))
