import argparse
import requests
import smtplib
import sys
import time
from email.mime.text import MIMEText

def mailgun_emailer(api, domain, filename, subject, sender, recipient, htmlbody, attachments):
	url = 'https://api.mailgun.net/v3/{}/messages'.format(domain)
	auth = ('api', api)
	data = {}
	files = {}

	with open(filename) as fp:

		if htmlbody:
			data = {
				'from':sender,
				'to':recipient,
				'subject':subject,
				'text': 'Please enable HTML to view contents of this e-mail.',
				'html': fp.read(),
			}
		else:
			data = {
				'from':sender,
				'to':recipient,
				'subject':subject,
				'text': MIMEText(fp.read()),
			}

		if attachments != "":
			response = requests.post(url, auth=auth, data=data, files=files)
			print("[!] Successfully sent API call to mailgun with attachment | Destination: %s", recipient)
		else:
			response = requests.post(url, auth=auth, data=data)
			print("[!] Successfully sent API call to mailgun | Destination: %s", recipient)

def gmail_emailer(username, password, filename, subject, sender, recipient):
	with open(filename) as fp:
		# Create a text/plain message
		body = fp.read()

		# Setup server
		s = smtplib.SMTP("smtp.gmail.com:587")
		s.ehlo()
		s.starttls()
		s.login(username, password)

		# Setup message
		msg = '\r\n'.join(['To: %s' % recipient,
							'From: %s' % sender,
							'Subject: %s' % subject,
							'', body])
		try:
			s.sendmail(sender, recipient, msg)
			print("[!] Successfully sent gmail | Destination: %s", recipient)
		except:
			print("[*] Error - could not send gmail | Destination: %s", recipient)

def postfix_emailer(filename, subject, sender, recipient):
	with open(filename) as fp:
		# Create a text/plain message
		msg = MIMEText(fp.read())
		msg['Subject'] = subject
		msg['From'] = sender
		msg['To'] = recipient

		# Send the message via our own SMTP server.
		s = smtplib.SMTP('localhost')
		
		try:
			s.send_message(msg)
			print("[!] Successfully sent postfix email | Destination: %s", recipient)
		except:
			print("[*] Error - could not send postfix email | Destination: %s", recipient)
			s.quit()

def email_controller(args, destination_email):
	# Decide where to route e-mails to
	if args.infrastructure == "mailgun":
		mailgun_emailer(args.api, args.domain, args.body, args.subject, args.email_author, destination_email, args.enable_html, args.attachment)
	elif args.infrastructure == "gmail":
		gmail_emailer(args.username, args.password, args.body, args.subject, args.email_author, destination_email)
	elif args.infrastructure == "postfix":
		postfix_emailer(args.body, args.subject, args.email_author, destination_email)
	else:
		print("[*] Error - incorrect infrastructure parameter.")

def banner():
	print("'||'  '||' '||''''|  '||''|.   '||    ||' '||''''|   .|'''.| ")
	print(" ||    ||   ||  .     ||   ||   |||  |||   ||  .     ||..  ' ")
	print(" ||''''||   ||''|     ||''|'    |'|..'||   ||''|      ''|||. ")
	print(" ||    ||   ||        ||   |.   | '|' ||   ||       .     '||")
	print(".||.  .||. .||.....| .||.  '|' .|. | .||. .||.....| |'....|' ")

def main():
	# Create initial definition of variables
	body = ""
	password = ""

	# Define arguments for the script
	parser     = argparse.ArgumentParser(description='Sends e-mails via a number of means.')
	#       Create groups
	required   = parser.add_argument_group("Required", "The following flags are required to run the script.")
	recipients = parser.add_argument_group("Recipients", "Select one method where the e-mail recipients will be found.")
	mailgun    = parser.add_argument_group("MailGun", "Please add the following flags to enable MailGun sending.")
	gmail      = parser.add_argument_group("Google Mail", "Please add the following flags to enable G-Mail sending.")
	postfix    = parser.add_argument_group("Postfix", "To use a local postfix there are no additional flags required. Just enable with '-i'.")
	optional   = parser.add_argument_group("Optional", "Use the following flags to manipulate the sending of e-mails")
	required.add_argument('-i','--infrastructure', help='Technology sending the e-mails (gmail, mailgun, local postfix)')
	required.add_argument('-b','--body', help='Textfile containing the body of the email')
	required.add_argument('-s','--subject', help='E-mail subject')
	required.add_argument('-f','--email-author', help='Sender of the e-mail')
	gmail.add_argument('-u','--username', help='Username to authenticate with')
	gmail.add_argument('-p','--password', help='Password to authenticate with')
	mailgun.add_argument('-a','--api', help="MailGun API key to authenticate with")
	mailgun.add_argument('--domain', help="Domain to send MailGun e-mail from")
	recipients.add_argument('-r','--recipient', help='Singular destination to send e-mail to.')
	recipients.add_argument('-l','--list-of-emails', help='Textfile containing a list of destination e-mails')
	optional.add_argument('-d', '--delay', help="Delay the sending of e-mails by a number of seconds.", type=int)
	optional.add_argument('--attachment', help="Add an attachment to the e-mail you're sending")
	optional.add_argument('--enable-html', help="Enable rich text e-mails. This will send rendered HTML in the e-mail.")

	args = parser.parse_args()

	if args.body and args.infrastructure and args.subject and args.email_author:
		# If passing the singular recipient e-mail
		if args.recipient:
			# If passing both arguments...
			if args.list_of_emails:
				print("[*] Error - passing wrong arguments. -r/--recipient and -l/--list-of-emails are mutually exclusive.")
				sys.exit(1)
			banner()
			email_controller(args, args.recipient)
		elif args.list_of_emails:
			with open(args.list_of_emails) as fp:
				for line in fp:
					banner()
					email_controller(args, line)
					if args.d:
						time.sleep(args.d)
		else:
			print("[*] Error - need to pass recipient(s). This can be done singular (-r) or through a textfile list (-l).")
	else:
		parser.print_help()
# Start Hermes
main()
