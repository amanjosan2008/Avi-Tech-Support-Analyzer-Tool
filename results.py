#!/usr/bin/python3
import os
import json
import re
import cgi, cgitb

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print ("""<html>
<head>
<title>Tech Support Debug Logs Analyzer</title>
</head>
<body style='background-color:d9d9d9;'>""")

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
path = form.getvalue('path')

dirlist = []

for root,dirc,files in os.walk(path):
    for filename in files:
       dirlist.append(os.path.join(os.path.realpath(root),filename))

#print("<h2>Results for %s</h2>") % (path)

# Versions Info
print("<h3>\n############ VERSION INFO #############\n</h3>")
for i in dirlist:
    if "VERSION" in i:
        if "prev" in i:
            print("<h4>Upgraded from:</h4>")
        else:
            print("<h4>Upgraded To:</h4>")
        f = open(i,'r')
        l = f.readlines()
        for j in range(len(l)):
            if re.match("Date",l[j]):
                print(l[j].rstrip('\n'),"<br />")
            if re.match("Tag",l[j]):
                print(l[j].rstrip('\n'),"<br />")
            if re.match("ProductName",l[j]):
                print(l[j].rstrip('\n'),"<br />\n")

# Avi Config Parser
for i in dirlist:
    if i.split('/')[-1] == "avi_config":
        f = open(i,'r')
        config = json.load(f)
        f.close
        #for i in range(len(config["ControllerLicense"][0]["license_tiers"])):
        #    print("License: ", i+1,"\n")
        #    for k,v in config["ControllerLicense"][0]["license_tiers"][i].items():
        #        print(k,v)
        #    print('\n')
        print("<h3>\n############ LICENSE INFO #############\n</h3>")
        print("<p>Max SEs: ", config["ControllerLicense"][0]["max_ses"],'</p>\n')
        a = 1
        for j in range(len(config["ControllerLicense"][0]["extension"]["used_license_resources"])):
            if config["ControllerLicense"][0]["extension"]["used_license_resources"][j]['license_type'] == 'LIC_CORES':
                print("Used Cores: LIC",a, ":" ,config["ControllerLicense"][0]["extension"]["used_license_resources"][j]['used_count'],"<br />")
                a += 1
        print('\n')

        for k in range(len(config["ControllerLicense"][0]["licenses"])):
            print("<h4>License File Name:", config["ControllerLicense"][0]["licenses"][k]["license_name"],"</h4>")
            print("Customer Name:", config["ControllerLicense"][0]["licenses"][k]["customer_name"],"<br />")
            print("License ID:", config["ControllerLicense"][0]["licenses"][k]["license_id"],"<br />")
            print("License Type:", config["ControllerLicense"][0]["licenses"][k]["license_type"],"<br />")
            print("Tier Type:", config["ControllerLicense"][0]["licenses"][k]["tier_type"],"<br />")
            print("Valid Till:", config["ControllerLicense"][0]["licenses"][k]["valid_until"],"<br />")
            print("Max SEs:", config["ControllerLicense"][0]["licenses"][k]["max_ses"],"<br />")
            print("Sockets:", config["ControllerLicense"][0]["licenses"][k]["sockets"],"<br />")
            print("Cores:", config["ControllerLicense"][0]["licenses"][k]["cores"],"<br />")
            print("\n")

        print("<h3>\n############ CLOUDS INFO #############\n</h3>")
        for l in range(len(config["Cloud"])):
            #print(config["Cloud"][l],'\n')
            print("<h4>Cloud Name:", config["Cloud"][l]["name"],"</h4>")
            print("Cloud Type:", config["Cloud"][l]["vtype"],"<br />")
            print("Cloud UUID:", config["Cloud"][l]["uuid"],"<br />")
            print("Tenant:", config["Cloud"][l]["tenant_ref"],"<br />")
            print("DHCP Enabled:", config["Cloud"][l]["dhcp_enabled"],"<br />")
            b = 1
            if config["Cloud"][l]["vtype"] == "CLOUD_LINUXSERVER":
                for k,v in config["Cloud"][l]["linuxserver_configuration"].items():
                    if k != "hosts":
                        print(k,': ',v,"<br />")
                    else:
                        for m in range(len(v)):
                            print("<h5>LSC: ", b,"</h5>")
                            b += 1
                            print(" -  IP Address: ", v[m]["host_ip"]["addr"],"<br />")
                            for n in range(len(v[m]["host_attr"])):
                                print(" - ",v[m]["host_attr"][n]['attr_key'], ": ",v[m]["host_attr"][n]['attr_val'],"<br />")

            elif config["Cloud"][l]["vtype"] == "CLOUD_VCENTER":
                print("Username: ", config["Cloud"][l]["vcenter_configuration"]['username'],"<br />")
                print("DataCenter: ", config["Cloud"][l]["vcenter_configuration"]['datacenter'],"<br />")
                print("Privilege: ", config["Cloud"][l]["vcenter_configuration"]['privilege'],"<br />")
                print("Vcenter URL: ", config["Cloud"][l]["vcenter_configuration"]['vcenter_url'],"<br />")
                print("No of Subnets Discovered:", len(config["Network"]),"<br />")
            print("<br />")


        print("<h3>\n############ POOL INFO #############\n</h3>")
        for m in range(len(config["Pool"])):
            print("<h4>Name: ",config["Pool"][m]["name"],"</h4>")
            print("Enabled: ",config["Pool"][m]["enabled"],"<br />")
            print("Max concurrent conns per server: ",config["Pool"][m]["max_concurrent_connections_per_server"],"<br />")
            print("UUID: ",config["Pool"][m]["uuid"],"<br />")
            print("LB Algorithm: ",config["Pool"][m]["lb_algorithm"],"<br />")
            print("Default server port: ",config["Pool"][m]["default_server_port"],"<br />")
            print("Tenantref: ",config["Pool"][m]["tenant_ref"],"<br />")
            print("VRF ref: ",config["Pool"][m]["vrf_ref"],"<br />")
            print("Cloud ref: ",config["Pool"][m]["cloud_ref"],"<br />")
            print("SNI enabled: ",config["Pool"][m]["sni_enabled"],"<br />")
            print("Rewrite host header to server name: ",config["Pool"][m]["rewrite_host_header_to_server_name"],"<br />")
            print("Rewrite host header to sni: ",config["Pool"][m]["rewrite_host_header_to_sni"],"<br />")
            try:
                print("Health monitor refs: ",config["Pool"][m]["health_monitor_refs"],"<br />")
            except:
                print("Health monitor refs: No Health Monitors attached to this Pool","<br />")
            print("Inline health monitor: ",config["Pool"][m]["inline_health_monitor"],"<br />")
            print("Server count: ",config["Pool"][m]["server_count"],"<br />")
            if config["Pool"][m]["server_count"] > 0:
                print("<h4>Servers Info: </h4>")
                for n in range(len(config["Pool"][m]["servers"])):
                    print("<h5>Hostname:", config["Pool"][m]["servers"][n]['hostname'],"</h5>")
                    print("IP Address:", config["Pool"][m]["servers"][n]['ip']['addr'],"<br />")
                    try:
                        print("Port:", config["Pool"][m]["servers"][n]['port'],"<br />")
                    except:
                        print("Port: Inherited")
                    print("Status:", config["Pool"][m]["servers"][n]['enabled'],"<br />")
                    print("Ratio:", config["Pool"][m]["servers"][n]['ratio'],"<br />")
                    print("Rewrite Host Header:", config["Pool"][m]["servers"][n]['rewrite_host_header'],"<br />")
            else:
                print("Servers: No Server attached to this Pool","<br />")
            print("<br />")

print("<h3>\n############ DONE #############\n</h3>")
print ("</body>")
print ("</html>")
