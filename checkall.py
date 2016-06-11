##################################################################################################################
# Program                        : checkall.py                                                                   #
# Description                    : A small program to send mail when it encounters a broken link and generates a #
#                                  spreadsheet containing details of the outage					 #													
# Author                         : Soutrik Chatterjee, AM(IT), Emp No - 5374                                     #
# Date Created                   : 29th February,2016                                                            #
# Date Last Modified             : 1st March, 2016		                                                 #
##################################################################################################################


import os
import smtplib
from excel_generate import generate_excel, write_to_excel
from smtplib import SMTPException

# List of ip addresses of BSNL MPLS network of all the plants  

device_ip = ["172.21.48.201","172.21.52.181","172.21.48.185","172.21.48.181","172.20.8.89","172.20.10.193","172.20.64.73","172.20.65.89"]

# List of locations 

device_location = ["STPS","STPS Township","BkTPP","SgTPP","BTPS","BTPS Township","KTPS","KTPS Township"] 

mail_sender = 's.chatterjee01@wbpdcl.co.in'					# Sender mail address
mail_receivers = ['chatterjee.soutrik@gmail.com'] 				# List of mail addresses of the receivers
smtp_object = smtplib.SMTP('mail.wbpdcl.co.in')  				# Create SMTP instance using SMTP server of the organization

file_object = open("event_count","r+w")


counter = 0
event_id = int(file_object.read(4))

#print device_location[0]

#generate_excel()

for ip in device_ip :
	
	response = os.system("ping -c 5 " + ip)
	
	if response == 0:
		
  		print device_location[counter], ip, 'is up!'
		counter = counter + 1

	else:
		try:
			print device_location[counter], ip, 'is down!'	 
  			subject = 'The WBPDCL ' + device_location[counter] + ' Link ( WAN IP ' + ip + ' ) Down '
			text = 'The WBPDCL ' + device_location[counter] + ' Link ( WAN IP ' + ip + ' )  is down. Please resolve ASAP.'

			mail_content = 'Subject: %s\n\n%s' % (subject, text)               # Create the message body

			write_to_excel(event_id, ip, device_location[counter])
			
   			smtp_object.sendmail(mail_sender, mail_receivers, mail_content)    # Send the mail     
   			print "Successfully sent email"
			
			counter = counter + 1
			event_id += 1
			
			file_object.seek(0)
			file_object.write(str(event_id))
			
		except SMTPException:

   			print "Error: unable to send email"
   			
file_object.close()
