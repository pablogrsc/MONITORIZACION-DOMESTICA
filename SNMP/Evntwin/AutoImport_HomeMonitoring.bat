echo 
REM ***************************************
REM * SNMP Server Alerts  				  *
REM * (c) 2020 Pablo M. Garcia Sanchez	  *
REM ***************************************

REM 
REM  Begin Importing Aplications & Systems Alerts

timeout /t 10

evntcmd /v 10 c:\snmp\cnf\appgp.cnf

evntcmd /v 10 c:\snmp\cnf\appmicrosoft.cnf

evntcmd /v 10 c:\snmp\cnf\appmisc.cnf

evntcmd /v 10 c:\snmp\cnf\appsystem.cnf

evntcmd /v 10 c:\snmp\cnf\systemmisc.cnf

evntcmd /v 10 c:\snmp\cnf\systemmswindows.cnf

evntcmd /v 10 c:\snmp\cnf\systemuefi.cnf

evntcmd /v 10 c:\snmp\cnf\appwinbak.cnf



REM Importing Security Alerts

timeout /t 5

evntcmd /v 10 c:\snmp\cnf\security.cnf



REM Stopping SNMP Service

net stop SNMP

timeout /t 5

REM Starting SNMP Service

net start SNMP

timeout /t 30



REM Logging Off...


Logoff


REM COMPLETED!
