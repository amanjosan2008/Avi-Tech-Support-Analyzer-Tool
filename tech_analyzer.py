#!/usr/bin/python3

# Import modules for CGI handling
import cgi, cgitb

print ("Content-type:text/html\r\n\r\n")
print ("""
<html>
<head>
<title>Tech Support Debug Logs Analyzer</title>
</head>
<body style='background-color:d9d9d9;'>
<form action = "/cgi-bin/results.py" method = "get">
Logs Location: <input type = "text" name = "path">  <br />
<input type = "submit" value = "Submit" />
</form>
</body>
</html>""")
