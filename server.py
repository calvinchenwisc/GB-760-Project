"""
File: server.py
Name: Calvin Chen
---------------------------
This file reads all the tweets from Twitter and write 
each text and timestamp to tweets.txt in the
following format:

tweet timestamp in YYYY-MM-DD-HH-MM-SS format, tweet text
"""
import tweepy
import time
import re
import json
import argparse
import spacy
import en_core_web_sm

consumer_key = '55iKh2vnoNjRNldmBRi1SAT3e'
consumer_secret = 'eFIqDQn8mkf0jaXB1PUgtjPHWmDqLewFJTJMVHdxkhcdrgPVKe'
access_key= '1435726675925405696-rPMEdVKvBBAIMVSWqioNfdf9Rlq0ef'
access_secret = 'NJAhAqMjYIyoAevVA7t8QWiboX1LVBwr513xNBTRokSyE' 
regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

nlp = spacy.load('en_core_web_sm',  disable=['parser', 'ner'])

class TweetPrinter(tweepy.Stream):
	fileWriter = open('tweets.txt', 'w', encoding='utf8')

	def disconnect(self):
		super()
		self.fileWriter.close()

	def clean_text(self, text):
		"""
		Clean the emoji from the text
		"""
	  	if type(text) != str:
	  		text = text.decode("utf-8")
	  	doc = re.sub(regex, '', text, flags=re.MULTILINE) # remove URLs
	  
	  	sentences = []
	  	for sentence in doc.split("\n"):
	  		if len(sentence) == 0:
	  			continue
	  		sentences.append(sentence)
	  	doc = nlp("\n".join(sentences))
	  	
	  	doc = " ".join([token.lemma_.lower().strip() for token in doc
	  					if (not token.is_stop)
	  						and (not token.like_url)
	  						and (not token.lemma_ == "-PRON-")
	  						and (not len(token) < 4)])
	  	 
	  	return doc


	def on_data(self, data):
		decodedData = json.loads(data)
		createdAt = decodedData['created_at']
		formattedCreatedAt = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(str(createdAt), "%a %b %d %H:%M:%S +0000 %Y"))
		text = decodedData['text']
		text = self.clean_text(text)

		log = ','.join([formattedCreatedAt,text])
		self.fileWriter.write(formattedCreatedAt+','+text+'\n')
		print(log)

	def on_connection_error(self):
		self.disconnect()


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file')
	args = parser.parse_args()

	if args.file is not None:
		pass
		# Here read from the json file
		# for line in args.file:
		# 	decodedData = json.loads(lines)
		# 	createdAt = decodedData['created_at']
		# 	formattedCreatedAt = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(str(createdAt), "%a %b %d %H:%M:%S +0000 %Y"))
		# 	text = decodedData['text']
		# 	text = self.clean_text(text)

	else:
		printer = TweetPrinter(consumer_key, consumer_secret,access_key, access_secret)
		try:			
			printer.sample(languages=['en'])
		except:
			printer.disconnect()


if __name__ == '__main__':
    main()