''' libraries used for sending/receiving emails '''
import smtplib
import poplib
from email import parser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import quotequail

''' A convienence wrapper for sending emails in python '''
class EmailManager:

	def __init__(self, email, password):

		# saves the email
		self.email = email
		self.password = password

		# starts the server
		self.server = smtplib.SMTP('smtp.gmail.com', 587)
		self.server.starttls()
		self.server.login(email, password)


	def send_email(self, to, subject, contents):

		print("Sending email to {email}".format(email=to))
	
		# creates a new email
		msg = MIMEMultipart()
		msg['From'] = 'Catan Bot <{}>'.format(self.email)
		msg['To'] = to
		msg['Subject'] = subject
		
		# creates new text
		body = MIMEText(contents, "plain")
		
		msg.attach(body)
		
		self.server.sendmail(self.email, to, msg.as_string())


	''' Gets all the emails from the server and returns them as an array of dictionaries
		Ex:
			[
				{
					"from": "some_email"
					"subject": "some_subject"
					"body": "some_body"
				}
			]
	'''

	def get_emails(self):
	
		# connects to gmail
		pop_conn = poplib.POP3_SSL('pop.gmail.com')
		pop_conn.user(self.email)
		pop_conn.pass_(self.password)

		# Get messages from server:
		messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
					
		# decodes them
		messages = ["\n".join(m.decode("utf-8") for m in mssg[1]) for mssg in messages]
		
		to_return = []
		
		# Parse message intom an email object:
		messages = [parser.Parser().parsestr(mssg) for mssg in messages]
		
		for message in messages:
			
			# gets the body for each message
			body = ""
			
			for part in message.walk():
				
				if part.get_content_type() == "text/plain":
					body = part.get_payload()
					break
			
			# removes previous messages, if any
			new_body = quotequail.unwrap(body)
			
			if new_body != None:
				body = new_body['text_top']
						

			to_return.append({
				"from": message['From'],
				"subject": message['Subject'],
				"body": body
			})

		pop_conn.quit()
		
		# returns the messages
		return to_return;
		