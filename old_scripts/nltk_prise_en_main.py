# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 22:48:47 2020

@author: romain
"""

import nltk 
nltk.data.path.append("D:\\Users\\romai\\nltk_data")
import pandas as pd
import re, pprint
import numpy as numpy
from nltk import word_tokenize
                
from nltk.book import * 

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

#Words in context
text1.concordance("monstruous")
text2.concordance("affection")

#What other words appear in a similar range of contexts
text2.similar("affection")

#Examine the contextes that are shared by two or more words
text2.common_contexts(["affection","very"])

#positional information can be displayed using 
#a dispersion plot. Each stripe represents an 
#instance of a word and each row represents the 
#entire text
text4.dispersion_plot(
        ["citizens", "democracy", "freedom", "duties", "America"])

#A collocation is a sequence of words that occur together unusually often. 
#Thus red wine is a collocation, whereas the wine is not. A characteristic of 
#collocations is that they are resistant to substitution with words that have 
#similar senses; for example, maroon wine sounds definitely odd.
#
#To get a handle on collocations, we start off by extracting from a text a
# list of word pairs, also known as bigrams. This is easily accomplished with the function bigrams():

a = list(bigrams(['more', 'is', 'said', 'than', 'done']))

def lexical_diversity(text):
    return len(set(text)) / len(text)

def percentage(count, total):
    return 100 * count / total

#part_of_speech tagging
# nltk.help.upenn_tagset('VBP') : meaning of tag 

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

#. 	Wildcard, matches any character
#^abc 	Matches some pattern abc at the start of a string
#abc$ 	Matches some pattern abc at the end of a string
#[abc] 	Matches one of a set of characters
#[A-Z0-9] 	Matches one of a range of characters
#ed|ing|s 	Matches one of the specified strings (disjunction)
#* 	Zero or more of previous item, e.g. a*, [a-z]* (also known as Kleene Closure)
#+ 	One or more of previous item, e.g. a+, [a-z]+
#? 	Zero or one of the previous item (i.e. optional), e.g. a?, [a-z]?
#{n} 	Exactly n repeats where n is a non-negative integer
#{n,} 	At least n repeats
#{,n} 	No more than n repeats
#{m,n} 	At least m and no more than n repeats
#a(b|c)+ 	Parentheses that indicate the scope of the operators
    
#\b 	Word boundary (zero width)
#\d 	Any decimal digit (equivalent to [0-9])
#\D 	Any non-digit character (equivalent to [^0-9])
#\s 	Any whitespace character (equivalent to [ \t\n\r\f\v])
#\S 	Any non-whitespace character (equivalent to [^ \t\n\r\f\v])
#\w 	Any alphanumeric character (equivalent to [a-zA-Z0-9_])
#\W 	Any non-alphanumeric character (equivalent to [^a-zA-Z0-9_])
#\t 	The tab character
#\n 	The newline character

f = open('document.txt', encoding='utf-8')
raw = f.read()

for line in f:
    print(line.strip())
    
tokens = word_tokenize(raw)
words = [w.lower() for w in tokens]
vocab = sorted(set(words))

# The relative character frequencies of a text can be used in automatically 
# identifying the language of the text.
fdist = nltk.FreqDist(ch.lower() for ch in raw if ch.isalpha())
fdist.most_common(5)
print([char for (char, count) in fdist.most_common()])

raw.find('bla') #index of first letter of string
#.find / .rfind / .indx / .rindex / .join / .split
# .splitlines / .lower / .upper / .title / .strip / .replace

#Regular Expressions for Detecting Word Patterns
wordlist = [w for w in nltk.corpus.words.words('en') if w.islower()]

# $ : end of a STRING 
#Look for words that end with 'ed'
[w for w in wordlist if re.search('ed$', w)]

# ^ : beginning of a STRING
#Look for 8-letters words with j as 3rd and t as 6th
[w for w in wordlist if re.search('^..j..t..$', w)]

#If we remove ^ and $ there can be more than 2 letters at the beggining and end
#of the seeked word
[w for w in wordlist if re.search('..j..t..', w)]

#Count the occurences of 'email' and 'e-mail' : here the '-' is optional
sum(1 for w in wordlist if re.search('^e-?mail$', w))

#Each set correspond to a character location, we look for all words matching any
#permuttion of these letters
[w for w in wordlist if re.search('^[ghi][mno][jlk][def]$', w)]

# '+' means "one or more instances of the preceding item"
# could be an individual character like m, a set like [fed] 
# or a range like [d-f]
chat_words = sorted(set(w for w in nltk.corpus.nps_chat.words()))
[w for w in chat_words if re.search('^m+i+n+e+$', w)]

# Here '\.' is simply a string point, so we look for all float numbers
wsj = sorted(set(nltk.corpus.treebank.words()))
[w for w in wsj if re.search('^[0-9]+\.[0-9]+$', w)]

# ^ inside a [] is an exclusion : [^aeiou] = any non lower vowel

# braced expressions, like {3,5}, specify the number of repeats of 
# the previous item
# First we look for all 4 digits numbers
# Second we look for all strings with this pattern XX-SSS, x digit and s letter
[w for w in wsj if re.search('^[0-9]{4}$', w)]
[w for w in wsj if re.search('^[0-9]+-[a-z]{3,5}$', w)]

#Looks for all words containing wit, wet, wait, and woot
[w for w in wordlist if re.search('w(i|e|ai|oo)t', w)]

#Find words with differents endings
[w for w in wsj if re.search('(ed|ing)$', w)]

#re.findall() ("find all") method finds all (non-overlapping) matches of the 
#given regular expression. Let's find all the vowels in a word, then count them:
word = 'supercalifragilisticexpialidocious'
re.findall(r'[aeiou]', word)
len(re.findall(r'[aeiou]', word))

# Let's look for all sequences of two or more vowels in some text, and determine
# their relative frequency:
wsj = sorted(set(nltk.corpus.treebank.words()))
fd = nltk.FreqDist(vs for word in wsj
                   for vs in re.findall(r'[aeiou]{2,}', word))
fd.most_common(12)

#The regular expression in our next example matches initial vowel sequences, 
#final vowel sequences, and all consonants; everything else is ignored
# re.findall() to extract all the matching pieces, and ''.join() to join them together
regexp = r'^[AEIOUaeiou]+|[AEIOUaeiou]+$|[^AEIOUaeiou]'
def compress(word):
    pieces = re.findall(regexp, word)
    print(pieces)
    return ''.join(pieces)

english_udhr = nltk.corpus.udhr.words('English-Latin1')
nltk.tokenwrap(compress(w) for w in english_udhr[:75])

#extract all consonant-vowel sequences from the words of Rotokas, such as ka and 
#si. Since each of these is a pair, it can be used to initialize a conditional 
#frequency distribution. We then tabulate the frequency of each pair
rotokas_words = nltk.corpus.toolbox.words('rotokas.dic')
cvs = [cv for w in rotokas_words for cv in re.findall(r'[ptksvr][aeiou]', w)]
cfd = nltk.ConditionalFreqDist(cvs)
cfd.tabulate()
#helpful to have an index, allowing us to quickly find the list of words that 
#contains a given consonant-vowel pair, e.g. cv_index['su'] should give us all 
#words containing su
cv_word_pairs = [(cv, w) for w in rotokas_words
                         for cv in re.findall(r'[ptksvr][aeiou]', w)]
cv_index = nltk.Index(cv_word_pairs)
cv_index['su']
cv_index['po']

#Find stems
#Here, re.findall() just gave us the suffix even though the regular expression 
#matched the entire word. This is because the parentheses have a second function
#, to select substrings to be extracted. If we want to use the parentheses to 
#specify the scope of the disjunction, but not to select the material to be 
#output, we have to add ?:, which is just one of many arcane subtleties of 
#regular expressions. Here's the revised version.
re.findall(r'^.*(ing|ly|ed|ious|ies|ive|es|s|ment)$', 'processing')
re.findall(r'^.*(?:ing|ly|ed|ious|ies|ive|es|s|ment)$', 'processing')
#However, we'd actually like to split the word into stem and suffix. So we 
#should just parenthesize both parts of the regular expression:
re.findall(r'^(.*)(ing|ly|ed|ious|ies|ive|es|s|ment)$', 'processing')
#The regular expression incorrectly found an -s suffix instead of an -es suffix. 
#This demonstrates another subtlety: the star operator is "greedy" and the .* part 
#of the expression tries to consume as much of the input as possible. If we use 
#the "non-greedy" version of the star operator, written *?, we get what we want
re.findall(r'^(.*)(ing|ly|ed|ious|ies|ive|es|s|ment)$', 'processes')
re.findall(r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)$', 'processes')
#This works even when we allow an empty suffix, by making the content of the 
#second parentheses optional:
re.findall(r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$', 'language')
#define a function to perform stemming, and apply it to a whole text
def stem(word):
    regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'
    stem, suffix = re.findall(regexp, word)[0]
    return stem

raw = """DENNIS: Listen, strange women lying in ponds distributing swords
is no basis for a system of government.  Supreme executive power derives from
a mandate from the masses, not from some farcical aquatic ceremony."""
tokens = word_tokenize(raw)

#You can use a special kind of regular expression for searching across multiple 
#words in a text (where a text is a list of tokens). For example, "<a> <man>" 
#finds all instances of a man in the text. The angle brackets are used to mark 
#token boundaries, and any whitespace between the angle brackets is ignored (
#behaviors that are unique to NLTK's findall() method for texts). In the 
#following example, we include <.*> [1] which will match any single token, 
#and enclose it in parentheses so only the matched word (e.g. monied) 
#and not the matched phrase (e.g. a monied man) is produced. The second 
#example finds three-word phrases ending with the word bro [2]. The last
#example finds sequences of three or more words starting with the letter l 
from nltk.corpus import gutenberg, nps_chat
moby = nltk.Text(gutenberg.words('melville-moby_dick.txt'))
moby.findall(r"<a> (<.*>) <man>") #[1]
chat = nltk.Text(nps_chat.words())
chat.findall(r"<.*> <.*> <bro>") #[2]
chat.findall(r"<l.*>{3,}") #[3]

#For instance, searching a large text corpus for expressions of the form x 
#and other ys allows us to discover hypernyms 
from nltk.corpus import brown
hobbies_learned = nltk.Text(brown.words(categories=['hobbies', 'learned']))
hobbies_learned.findall(r"<\w*> <and> <other> <\w*s>")
#Use TokenSeacher to assign the result of findall call to variable
from nltk.text import TokenSearcher
TokenSearcher(hobbies_learned).findall(r"<\w*> <and> <other> <\w*s>")

#3.6   Normalizing Text
#Stemmers
raw = """DENNIS: Listen, strange women lying in ponds distributing swords
is no basis for a system of government.  Supreme executive power derives from
a mandate from the masses, not from some farcical aquatic ceremony."""
tokens = word_tokenize(raw)
#NLTK includes several off-the-shelf stemmers, and if you ever need a stemmer 
#you should use one of these in preference to crafting your own using regular 
#expressions, since these handle a wide range of irregular cases. The Porter 
#and Lancaster stemmers follow their own rules for stripping affixes
porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()
[porter.stem(t) for t in tokens]
[lancaster.stem(t) for t in tokens]
#Lemmatization
#The WordNet lemmatizer only removes affixes if the resulting word is in its 
#dictionary. This additional checking process makes the lemmatizer slower than 
#the above stemmers. Notice that it doesn't handle lying, but it converts women 
#to woman. 
#The WordNet lemmatizer is a good choice if you want to compile the vocabulary 
#of some texts and want a list of valid lemmas (or lexicon headwords).
wnl = nltk.WordNetLemmatizer()
[wnl.lemmatize(t) for t in tokens]

#Tokenizing text
#The very simplest method for tokenizing text is to split on whitespace. 
#Consider the following text from Alice's Adventures in Wonderland:
raw = """'When I'M a Duchess,' she said to herself, (not in a very hopeful tone
though), 'I won't have any pepper in my kitchen AT ALL. Soup does very
well without--Maybe it's always pepper that makes people hot-tempered,'..."""
re.split(r'\s+', raw)  #re.split(r'[ \t\n]+', raw) 
re.split(r'\W+', raw) #split on all non alphanumeric characters
#Let's generalize the \w+ in the above expression to permit word-internal hyphens 
#and apostrophes: «\w+([-']\w+)*». This expression means \w+ followed by zero or 
#more instances of [-']\w+; it would match hot-tempered and it's. 
#(We need to include ?: in this expression for reasons discussed earlier.) 
#We'll also add a pattern to match quote characters so these are kept separate 
#from the text they enclose.
re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", raw)

#The function nltk.regexp_tokenize() is similar to re.findall() (as we've been 
#using it for tokenization). However, nltk.regexp_tokenize() is more efficient
#for this task, and avoids the need for special treatment of parentheses. For 
#readability we break up the regular expression over several lines and add a 
#comment about each line. The special (?x) "verbose flag" tells Python to strip 
#out the embedded whitespace and comments.
text = 'That U.S.A. poster-print costs $12.40...'
pattern = r'''(?x)     # set flag to allow verbose regexps
    (?:[A-Z]\.)+       # abbreviations, e.g. U.S.A.
  | \w+(?:-\w+)*       # words with optional internal hyphens
  | \$?\d+(?:\.\d+)?%? # currency and percentages, e.g. $12.40, 82%
  | \.\.\.             # ellipsis
  | [][.,;"'?():-_`]   # these are separate tokens; includes ], [
'''
nltk.regexp_tokenize(text, pattern)















