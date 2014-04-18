import os

# traverse the directory from root with os.walk(".")	
# note - relative to cmd if you do the above
for root, dirs, files in os.walk("d:\\prep"):
	# print the file and path with :: print (item) 
	for file in files:
	
		# build path to file on filesystem
		filepath = os.path.join(root, file)
		
		# open file to read 
		fh = open(filepath, 'r')
		lines = fh.readlines()
		# rewind
		fh.seek(0)
		original_file = fh.read()
				
		# create metadata XML block
		# init stringbuffer for XML
		sb = []
		sb.append('</FullText>')		
		sb.append('<Metadata>')
		sb.append('<FilePath>'+filepath+'</FilePath>')
		for line in lines:
			if line.startswith("Date: "):
				sb.append('<Date>'+line[6:].strip()+'</Date>')
			if line.startswith("From: "):
				sb.append('<From>'+line[6:].strip()+'</From>')
			if line.startswith("To: "):
				sb.append('<To>'+line[4:].strip()+'</To>')
			if line.startswith("Subject: "):
				sb.append('<Subject>'+line[9:].strip()+'</Subject>')
		sb.append('</Metadata></Item>')
		fh.close()
		
		# prepend file with xml opening elements (<Item><FullText>)
		with open(filepath, "w") as fhw:
			fhw.write('<Item><FullText>' + original_file) 
		
		
		# open file in append mode and add the metadata
		with open(filepath, "a") as fhw:
			fhw.write("\n".join(sb))
