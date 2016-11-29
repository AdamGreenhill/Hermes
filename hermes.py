import argparse
import logging
import requests
import smtplib
import sys
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

def process_message(string, find_str, replace_str):
	return string.replace(find_str, str(replace_str))

def create_message(subject, sender, recipient, body, encoding, attachment, increment, find_str, replace_str):
	# Establish MIME message
	msg            = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From']    = sender
	msg['To']      = recipient

	if increment is not None:
		body = process_message(body, find_str, replace_str)

	if str(encoding).lower() == "html":
		msg.attach(MIMEText('Please enable HTML to view this e-mail.', 'plain'))
		msg.attach(MIMEText(body, 'html'))
	else:
		msg.attach(MIMEText(body, 'plain'))

	if attachment is not None:
		with open(attachment, "rb") as fp:
			part = MIMEApplication (
					fp.read(),
					Name=basename(f)
				)
			part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
			msg.attach(part)

	return msg

def mailgun_emailer(api, domain, filename, subject, sender, recipient, encoding, attachment, increment, find_str, replace_str, verbose):
	url = 'https://api.mailgun.net/v3/{}/messages'.format(domain)
	auth = ('api', api)
	data = {}
	files = {}
	body = fp.read()
	
	if increment is not None:
		body = process_message(body, find_str, replace_str)

	with open(filename) as fp:

		if str(encoding).lower() == "html":
			data = {
				'from':sender,
				'to':recipient,
				'subject':subject,
				'text': 'Please enable HTML to view contents of this e-mail.',
				'html': body,
			}
		else:
			data = {
				'from':sender,
				'to':recipient,
				'subject':subject,
				'text': body,
			}

		if attachment is not None:
			files = [(basename(attachment), open(attachment))]
			response = requests.post(url, auth=auth, data=data, files=files)
			print("[!] Successfully sent API call to mailgun with attachment | Destination: %s" % recipient)
		else:
			response = requests.post(url, auth=auth, data=data)
			print("[!] Successfully sent API call to mailgun | Destination: %s" % recipient)

def gmail_emailer(username, password, filename, subject, sender, recipient, encoding, attachment, increment, find_str, replace_str, verbose):
	with open(filename) as fp:
		# Create a text/plain message
		body = fp.read()

		# Setup server
		s = smtplib.SMTP("smtp.gmail.com:587")
		s.ehlo()
		s.starttls()
		s.login(username, password)

		# Setup message
		msg = create_message(subject, sender, recipient, body, encoding, attachment, increment, find_str, replace_str)
		
		# Attempt to send e-mail
		try:
			s.sendmail(sender, recipient, msg.as_string())
			print("[!] Successfully sent gmail | Destination: %s" % recipient)
			s.quit()

		# Catching errors
		except Exception as e:
			error_str = "[*] Error - could not send gmail | Destination: %s" % recipient
			if verbose:
				logging.exception(error_str)
			else:
				print(error_str)

def basic_emailer(filename, subject, sender, recipient, host, encoding, attachment, increment, find_str, replace_str, verbose):
	with open(filename) as fp:
		# Create a text/plain message
		msg = create_message(subject, sender, recipient, body, encoding, attachment, increment, find_str, replace_str)

		# Send the message via our own SMTP server.
		s = smtplib.SMTP(host)
		
		try:
			s.send_message(msg)
			print("[!] Successfully sent postfix email | Destination: %s" % recipient)
			s.quit()
		except Exception as e:
			error_str = "[*] Error - could not send postfix email | Destination: %s" % recipient
			if verbose:
				logging.exception(error_str)
			else:
				print(error_str)

def email_controller(args, destination_email, find_str, replace_str):
	# Decide where to route e-mails to
	if args.infrastructure == "basic":
		basic_emailer(args.body, args.subject, args.email_author, destination_email, args.host, args.encoding, args.attachment, args.increment, find_str, replace_str, args.verbose)
	elif args.infrastructure == "gmail":
		gmail_emailer(args.username, args.password, args.body, args.subject, args.email_author, destination_email, args.encoding, args.attachment, args.incrementor, find_str, replace_str, args.verbose)
	elif args.infrastructure == "mailgun":
		mailgun_emailer(args.api, args.domain, args.body, args.subject, args.email_author, destination_email, args.encoding, args.attachment, args.increment, find_str, replace_str, args.verbose)
	else:
		print("[*] Error - incorrect infrastructure parameter.")

def banner():
	print("'||'  '||' '||''''|  '||''|.   '||    ||' '||''''|   .|'''.| ")
	print(" ||    ||   ||  .     ||   ||   |||  |||   ||  .     ||..  ' ")
	print(" ||''''||   ||''|     ||''|'    |'|..'||   ||''|      ''|||. ")
	print(" ||    ||   ||        ||   |.   | '|' ||   ||       .     '||")
	print(".||.  .||. .||.....| .||.  '|' .|. | .||. .||.....| |'....|' ")
	print("")

def main():
	# Create initial definition of variables
	body = ""
	counter = 0
	password = ""
	find_str = "{}"
	replace_str = 0

	# Define arguments for the script
	parser     = argparse.ArgumentParser(description='Sends e-mails via a number of means.')
	#       Create groups
	required   = parser.add_argument_group("Required", "The following flags are required to run the script.")
	recipients = parser.add_argument_group("Recipients", "Select whether the e-mail will be sent to a single recipient or multiple.")
	basic    = parser.add_argument_group("Basic SMTP", "Please add the following flags to enable Basic SMTP / Postfix sending.")
	gmail      = parser.add_argument_group("Google Mail", "Please add the following flags to enable G-Mail sending.")
	mailgun    = parser.add_argument_group("MailGun", "Please add the following flags to enable MailGun sending.")
	optional   = parser.add_argument_group("Optional", "Use the following flags to manipulate the sending of e-mails")
	required.add_argument('-i','--infrastructure', help='Technology sending the e-mails (gmail, mailgun, local postfix)')
	required.add_argument('-b','--body', help='Textfile containing the body of the email')
	required.add_argument('-s','--subject', help='E-mail subject')
	required.add_argument('-f','--email-author', help='Sender of the e-mail')
	basic.add_argument('--host', help='IP Address of SMTP server')
	gmail.add_argument('-u','--username', help='Username to authenticate with')
	gmail.add_argument('-p','--password', help='Password to authenticate with')
	mailgun.add_argument('-a','--api', help="MailGun API key to authenticate with")
	mailgun.add_argument('--domain', help="Domain to send MailGun e-mail from")
	recipients.add_argument('-r','--recipient', help='Singular destination to send e-mail to.')
	recipients.add_argument('-l','--list-of-emails', help='Textfile containing a list of destination e-mails')
	optional.add_argument('-d', '--delay', help="Delay the sending of e-mails by a number of seconds.", type=int)
	optional.add_argument('--attachment', help="Add an attachment to the e-mail you're sending")
	optional.add_argument('-e', '--encoding', help="Select how the e-mail will be encoded: html, plain. (default: plain)")
	optional.add_argument('-v', '--verbose', help="Print SMTP errors when they occur", default=False, action='store_true')
	optional.add_argument('--incrementor', help="Find, increment, and replace a value in an e-mail. The passed number represents the starting point.", type=int)

	args = parser.parse_args()

	if args.incrementor:
		replace_str = args.incrementor

	if args.body and args.infrastructure and args.subject and args.email_author:
		# If passing the singular recipient e-mail
		if args.recipient:
			banner()
			# If passing both arguments...
			if args.list_of_emails:
				print("[*] Error - passing wrong arguments. -r/--recipient and -l/--list-of-emails are mutually exclusive.")
				sys.exit(1)
			email_controller(args, args.recipient, find_str, replace_str)
		elif args.list_of_emails:
			banner()
			with open(args.list_of_emails) as fp:
				for line in fp:
					email_controller(args, line, find_str, replace_str + counter)
					if args.delay:
						time.sleep(args.delay)
					counter = counter + 1
		else:
			print("[*] Error - need to pass recipient(s). This can be done singular (-r) or through a textfile list (-l).")
	else:
		parser.print_help()
# Start Hermes
main()
