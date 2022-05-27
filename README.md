<div id="top"></div>
<h2>JSON2RAML Script</h2>

<h3>About The Project</h3>
<p>A RAML API specification details the functional and expected behavior of an API, as well as the fundamental design philosophy and supported data types. It contains both documentation and API definitions to create a contract that people and software can read.</p>
<p>It takes a tedious amount of time to manually code a RAML specification especially when the JSON contains too many fields. This "JSON2RAML" python utility automatically converts the JSON to RAML specification and generates a zip file that can be uploaded into the anypoint platform design center. This utility saves at least 70 to 100% of your time in coding the RAML spec.</p>

<p>This JSON to RAML converter utility was developed by <a href="https://www.folkstalk.com/2022/05/json-to-raml-converter-tool.html">Folkstalk.com</a></p>

<h3>Instructions to setup JSON2RAML utility</h3>
<ul>
  <li>Download and install python on your machine. Python Download <a href="https://www.python.org/downloads/">link</a>.</li>
  <li>Download the attached JSON2RAML.py file on your machine.</li>
</ul>

<h3>How to use JSON2RAML utility</h3>

<ul>
<li>Create a directory (call this as root) and within this create directories with endpoint names.</li>
<li>Rename the request and response JSON files to request.json and response.json respectively.</li>
<li>Copy these JSON files into respective endpoint directories.</li>
</ul>
<pre>
An example directory structure is
--rootDir--
---------Endpoint1--
------------------request.json--
------------------response.json--
---------Endpoint2--
------------------request.json--
------------------response.json--
</pre>
<ul>
<li>The JSON2RAML.py utility takes two arguments. The first argument is the RAML title and the second argument is the root directory path.</li>
<li>Open the command prompt and run the below command.</li>
<li>python JSON2RAML.py "RAML Title" "C:\Desktop\rootDir".</li>
<li>This will automatically creates the RAML spec as a zip file with name as “RAML Title.zip” in the root directory.</li>
<li>In the design center, there is an option to upload the RAML zip file. Use this option to create a new API specification.</li>
