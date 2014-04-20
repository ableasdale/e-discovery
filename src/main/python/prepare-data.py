import os
import http.client
import time, datetime
import concurrent.futures
from base64 import b64encode

# This will add XML content to the 'text/plain' enron email files and send them over to MarkLogic via an HTTP 'PUT' request
# c:\Python34\python.exe e-discovery\src\main\python\prepare-data.py

# ORIGINAL_DATA_DIR = "E:\\enron_corpus\\enron_mail_20110402"
ORIGINAL_DATA_DIR = "E:\\enron_corpus\\tmp"
REST_SERVER_PORT = 8003
HOSTNAME = "localhost"
ADMIN_USER = "q"
ADMIN_PASSWORD = "q"
CREDENTIALS = bytes((ADMIN_USER+':'+ADMIN_PASSWORD), encoding='utf-8') 

def process_file(filepath):
	xmldoc = filepath + '.xml'
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
	for line in lines[0:10]:		
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
		fhw.close()
	
	# open file in append mode and add the metadata
	with open(xmldoc, "a") as fhw:
		fhw.write("\n".join(sb))
		fhw.close()
	
	# put data
	http_put_file(xmldoc)
	
	#delete XML file - note that os.unlink(xmldoc) should also work
	try:
		os.remove(xmldoc)
	except OSError as e: 
		print ("Failed with:", e.strerror)
		print ("Error code:", e.code) 		

def http_put_file(filename):
	connection = http.client.HTTPConnection(HOSTNAME, REST_SERVER_PORT)
	userAndPass = b64encode(CREDENTIALS).decode("ascii")
	headers = { 'Authorization' : 'Basic %s' %  userAndPass, 'Content-type' : 'application/xml' }	
	f = open(filename, 'rb')
	try:
		connection.request('PUT', '/v1/documents?uri='+filename.replace("\\", "/"), f, headers)	
	except OSError as e: 
		print ("Failed with:", e.strerror)
		print ("Error code:", e.code)
	finally:
		f.close()
	response = connection.getresponse()	
	if response.status != 204 and response.status != 201:
		print("EXCEPTION: " + filename + " | " + str(response.status) + " | " + response.reason + " | "  + response.read().decode())
	
# initialise a Thread Pool (128 worker threads) for concurrent operations
executor = concurrent.futures.ThreadPoolExecutor(max_workers=128)

# traverse the directory from a given root with os.walk(".")	
for root, dirs, files in os.walk(ORIGINAL_DATA_DIR):
	# print the file and path with :: print (item) 
	for file in files:
                # task a single thread with the processing for that file
                executor.submit(process_file, os.path.join(root, file))
