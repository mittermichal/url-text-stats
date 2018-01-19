from collections import Counter
import nltk
from flask import Flask, request, render_template
import urllib.request
import lxml.html
#from bs4 import BeautifulSoup


#urllib.request.urlopen("http://google.com").read()
#html = lxml.html.fromstring('<div><p>test</p>b<p>v</p></div>')
#html = '<div><p>test</p>b<p>' \
#       'v</p></div>'
#soup = BeautifulSoup(html,"lxml")
#print(html.text_content())
#print(soup.get_text())
#import sys
#sys.exit()

def analyze_text(text):
    text=text.lower()
    result={}
    #words=text.split()
    words=nltk.word_tokenize(text)
    chars_only=list(filter(lambda c: c.isalpha(),text))

    letter_count = Counter(chars_only)
    word_count = Counter(words)

    result['most_frequent_letter']=letter_count.most_common(1) #https://docs.python.org/2/library/collections.html#collections.Counter.most_common
    result['longest_word'] = max(list(word_count), key=lambda x:len(x)) if list(word_count) else None
    result['word_frequency']=dict(word_count)

    return result

flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        url = request.form.get('url')
        data = urllib.request.urlopen(url).read()
        #soup = BeautifulSoup(data,"lxml")
        html=lxml.html.fromstring(data)
        #text=soup.get_text()
        text=html.text_content()
        return render_template('output.html',result=analyze_text(text))

if __name__ == "__main__":
  flask_app.run(port=7777, host='0.0.0.0', debug=True)