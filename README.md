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
To start using Hermes, there are a number of required flags that need to be used.
- `--infrastructure`|`-i` the infrastructure sending the e-mails. Options: basic, gmail, minigun
- `--body`|`-b` textfile containing the body of the e-mail
- `--subject`|`-s` e-mail subject
- `--email-author`|`-f` sender of the e-mail

The next required flag is choosing the recipient(s). This can be done in one of two ways:
- `--recipient`|`-r` a singular e-mail
- `--list-of-recipients`|`-l` textfile with e-mails separated by newlines

Depending on what infrastructure you plan to use, there are certain flags that need to be present.
- Basic SMTP / Postfix
	- `--host` IP address of the SMTP server
- Google Mail / Google for Work
	- `--username`|`-u` username to authenticate with
	- `--password`|`-p` password to authenticate with
- MailGun
	- `--api`|`-a` MailGun API key to authenticate with
	- `--domain` Domain to send MailGun e-mail from

Optionally, there are some modifier flags:
- `--delay`|`-d` delay the sending of e-mails by the given number of seconds
- `--attachment` add an attachment to the e-mail being sent (not available for gmail, basic at present)
- `--encoding`|`-e` change how the e-mail will be received. Options: html, plain
- `--verbose`|`-v` print SMTP errors as they occur 

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
