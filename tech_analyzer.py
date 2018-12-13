#!/usr/bin/python3

# Import modules for CGI handling
import cgi, cgitb

print ("Content-type:text/html\r\n\r\n")
print ("<html>")
print ("<head>")
print ("<title>Tech Support Debug Logs Analyzer</title>")
print ("</head>")
print ("<body>")
print('<form action = "/cgi-bin/results.py" method = "get">')
print('Logs Location: <input type = "text" name = "path">  <br />')
print('<input type = "submit" value = "Submit" />')
print("</form>")
print ("</body>")
print ("</html>")
