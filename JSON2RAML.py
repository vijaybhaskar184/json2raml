import sys
import os
import json
import shutil

#functions
def help():
	print("Help Document")
	print("Create a root directory and within this create directories with end point names.")
	print("Rename the request and response json files to request.json and response.json and place both the files in each endpoint directory")
	print("Example directory structure")
	print("--rootDir--")
	print("---------Endpoint1--")
	print("------------------request.json--")
	print("------------------response.json--")
	print("---------Endpoint2--")
	print("------------------request.json--")
	print("------------------response.json--")
	print("Pass the below arguments to this script.")
	print("Arg1: RAML Title")
	print("Arg2: Directory path to endpoint folders")
	print('Example: python JSON2RAML.py "Hello World" "C:\\Users\\vijayb\\Desktop\\python\\rootDir"')
	exit()
	
def fileHandle(jsonFile, type):
	try:
		dataFile = open(jsonFile, "r")
		data = dataFile.read()
		dataFile.close()
		return data
	except:
		print(type,".json file do not exists in the given directory", dir)
	return ""
	
def toJson(jsonString, type):
	try:
		data = json.loads(jsonString)
	except:
		print(type,".json is not a valid json file")
		exit()
	return data

#Dont edit this. Converts json 2 raml and displays the result.
def convert2raml(data, type, indent, result):
	space = " "
	if(isinstance(data, list)): 
		#print("array")
		result = result + space*indent + "type: array\n"
		if( len(data) > 0 ):
			result = result + space*indent + "items:\n"
			indent = indent + 2

			return convert2raml(data[0], type, indent, result)
	elif(isinstance(data, dict) and data != None):
		#print("object")
		result = result + space*indent + "type: object\n"
		result = result + space*indent + "properties:\n"
		indent = indent + 2
		eachObj = ""
		for key, value in data.items():
			eachObj = eachObj + space*indent + key + ":\n"
			if(isinstance(value,dict) or isinstance(value,list)):
				indent = indent + 2
			eachObj = eachObj + convert2raml(value, type, indent, "")
			if(isinstance(value,dict) or isinstance(value,list)):
				indent = indent - 2
		result = result + eachObj
	else:
		indent = indent + 2
		result = result + space*indent + "type: string\n"
		result = result + space*indent + "required: false\n"
		result = result + space*indent + "example: " + str(data) + "\n"
		return result
	return result
	
#Json 2 Raml Function and writes to files
def json2raml(data, type, indent, result, fileref):
	space = " "
	if(isinstance(data, list)): 
		#print("array")
		#indent = 0
		arrayStr = space*indent + "type: array\n"
		arrayStr = arrayStr + space*indent + "items:\n"
		fileref.write(arrayStr)
		if( len(data) > 0 ):
			indent = indent + 2		
			return json2raml(data[0], type, indent, result, fileref)
	elif(isinstance(data, dict) and data != None):
		if( fileref == ""):
			fileref = open(workingDir + "\\" + workingFile, "w")
			fileref.write(ramlDataType)
		#print("object")
		initObj = space*indent + "type: object\n" + space*indent + "properties:\n"
		fileref.write(initObj)
		indent = indent + 2
		eachObj = ""
		for key, value in data.items():
			keyString = space*indent + key + ":"
			if(isinstance(value,dict) or isinstance(value,list)):
				fileref.write(keyString + " !include " + key + ".raml\n")
				fh = open(workingDir + "\\" + key + ".raml", "w")
				fh.write(ramlDataType)
				#indent = 0
				recursiveStr = json2raml(value, type, 0, "", fh)
			else:
				keyString = keyString + "\n"
				fileref.write(keyString)
				recursiveStr = json2raml(value, type, indent, "", fileref)
			eachObj = eachObj + keyString
			fileref.write(recursiveStr)
			eachObj = eachObj + recursiveStr
			if(isinstance(value,dict) or isinstance(value,list)):
			    #indent = indent + 2
				None
	else:	
		if( isinstance(data,int) ):
			dataType = "number"
		else:
			dataType = "string"
			
		indent = indent + 2
		indKey = space*indent + "type: " + dataType + "\n"
		indKey = indKey + space*indent + "required: false\n"
		#indKey = indKey + space*indent + "example: '" + str(data) + "'\n"
		return indKey
	return result
			

def ramlFile(title, endpointArray):
	ramlString = """\
#%RAML 1.0
title: {ramlTitle}
description:
mediaType: application/json
version: v1

protocols: [ HTTPS ]

traits:
  client-id-required:
    headers:
      client_id:
        type: string
      client_secret:
        type: string

types:
""".format(ramlTitle = title)

	for ep in endpointArray:
		ramlTypes = """\
  {endpoint}-request: !include {endpoint}-request/request.raml
  {endpoint}-response: !include {endpoint}-response/response.raml
""".format(endpoint = ep)
		ramlString = ramlString + ramlTypes
	
	ramlString = ramlString + "\n"
	for ep in endpointArray:
		ramlEndPoint = """\
/{endpoint}:
  description:
  post:
    is: [client-id-required]
    body:
      application/json:
        type: {endpoint}-request
        example: !include examples/{endpoint}-request.raml
    responses:
      200:
        body:
          application/json:
            type: {endpoint}-response
            example: !include examples/{endpoint}-response.raml
""".format(endpoint = ep)
		ramlString = ramlString + ramlEndPoint
		
	fh = open(outDir + "\\" + title + ".raml", "w")
	fh.write(ramlString)
	fh.close()
	#print(ramlString)

def ramlExample(data, file):
	exampleHeader = "#%RAML 1.0 NamedExample"
	fh = open(examplesDir + "\\" + file + ".raml", "w")
	fh.write(exampleHeader + "\n\n")
	json.dump(data, fh, indent=4)
	fh.close()
	
def main():
	global outDir, workingDir, workingFile, examplesDir, ramlDataType
	args = sys.argv
	numArgs = len(args) - 1
	if( numArgs != 2 ):
		help()
	ramlTitle = args[1]
	filesDir = args[2]
	outDir = filesDir + "\\output"
	#requestDir = outDir + "\\" + "request"
	#responseDir = outDir + "\\" + "response"
	examplesDir = outDir + "\\" + "examples"
	requestJson = filesDir + "\\request.json"
	responseJson = filesDir + "\\response.json" 
	
	if(not os.path.exists(outDir)):
		os.makedirs(outDir)
	if(not os.path.exists(examplesDir)):
		os.makedirs(examplesDir)
	#if(not os.path.exists(requestDir)):
	#	os.makedirs(requestDir)
	#if(not os.path.exists(responseDir)):
	#	os.makedirs(responseDir)
		
	endPointArray = [name for name in os.listdir(filesDir) if(os.path.isdir(filesDir + "\\" + name) and name != 'output')]
	ramlFile(ramlTitle, endPointArray )
	
	for ep in endPointArray:
		endPointFiles = [name for name in os.listdir(filesDir + "\\" + ep) if(os.path.isfile(filesDir + "\\" + ep + "\\" + name))]
		for ef in endPointFiles:
			workingDir = outDir + "\\" + ep + "-" + (ef.split('.'))[0]
			if(not os.path.exists(workingDir)):
				os.makedirs(workingDir)
			workingFile = (ef.split('.'))[0] + ".raml"
			ramlDataType = "#%RAML 1.0 DataType\n\n"
			data = fileHandle(filesDir + "\\" + ep + "\\" + ef, "request")
			jsonData = toJson(data, "request")
			ramlExample(jsonData, ep + "-" + (ef.split('.'))[0])
			result = json2raml(jsonData, "request", 0, "","")
			#print(result)
			
	##Zip file
	shutil.make_archive(filesDir + "\\" + ramlTitle, 'zip', outDir)
	
	print("Raml File Generation is Completed. Zip file is located at ", filesDir)
	print("Import the '",ramlTitle, "' zip file into Anypoint platform")
	print("After Importing, make the '", ramlTitle,"' .raml file as root file")
		

main()