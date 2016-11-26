# ![Hermes](https://i.imgur.com/LnjMbGf.png)
Hermes is the swiss army knife of sending command line e-mails.

Features:
  - Send e-mails via Basic SMTP, Google Mail, MailGun
  - Send e-mails to a list of recipients
  - Send e-mails with a delay between sending

## Setup
- Install Python 3 and Python Pip: `sudo apt-get install python3 && sudo apt-get install python3-pip`
- Install Requests: `pip3 install requests`

## Usage
1. First

## Examples
### Basic SMTP / Postfix
```
python3 emailer.py -i basic 				\
	-b email_contents.txt 					\ 
	-s "Subject of e-mail" 					\
	-f "Author of E-mail"					\
	-r recipient@email.com 		 			\
	--host "IP Address of SMTP server"
```

### Google Mail / Google for Work
```
python3 emailer.py -i gmail 				\
	-b email_contents.txt 					\ 
	-s "Subject of e-mail" 					\
	-f "Author of E-mail"					\
	-r recipient@email.com 		 			\
	-u '<input your gmail e-mail>' 			\
	-p '<input your gmail password>'		
```
### MailGun
```
python3 emailer.py -i mailgun 				\
	-b email_contents.txt 					\ 
	-s "Subject of e-mail" 					\
	-f "Author of E-mail"					\
	-r recipient@email.com 		 			\
	-a '<MailGun API key>' 		 			\
	-d '<domain of e-mail>' 				
```
## Common errors
- Google will return an error if the account does not have [Less Secure Apps](https://www.google.com/settings/security/lesssecureapps) enabled 
- Your firewall may prevent the script from connecting directly to an SMTP server

## Contribute
Spotted a bug? Want to add features? Increase the performance?

Open an [issue](https://github.com/AdamGreenhill/Hermes/issues) or submit a [pull request](https://github.com/AdamGreenhill/Hermes/pulls)!

## License
This project is released under [The MIT License](LICENSE).
