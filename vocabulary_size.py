"""
File: vocabulary_size.py
Name: Calvin Chen
---------------------------
This file computes and prints the number of unique words
used in all the tweets stored in tweets.txt
"""

filename = 'tweets.txt'

WORD_DICT = {}			# store the unique word and the frequency of that word


def count_freq_word(line):
	"""
	Count the frequency of the words from the input tweets
	Input:
		line (str): timestamp and text in each tweet
	"""
	
	word_ls = line[1].split(" ")  
	for word in word_ls:

		if word not in WORD_DICT:
			if '@' in word:
				pass
			else:
				WORD_DICT[word] = 1   
		else:
			pass


def main():

	# read the file
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			line_l = line.split(",")
			count_freq_word(line_l)

	print('The number of unique words:', len(WORD_DICT))
 

if __name__ == '__main__':
    main()
	
