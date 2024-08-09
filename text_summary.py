import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """he Indian Premier League (IPL), also known as the TATA IPL for sponsorship reasons, is a men's Twenty20 (T20) cricket league held annually in India. Founded by the BCCI (the Board of Control for Cricket in India) in 2007, the league features ten city-based franchise teams.[3][4] The IPL usually takes place during the summer, between March and May each year. It has an exclusive window in the ICC Future Tours Programme, resulting in fewer international cricket tours occurring during the IPL seasons.[5]

The IPL is by far the most popular cricket league in the world; in 2014, it ranked sixth in average attendance among all sports leagues.[6] In 2010, the IPL became the first sporting event to be broadcast live on YouTube.[7][8] Inspired by the success of the IPL, other Indian sports leagues have been established.[a][11][12][13] In 2022, the league's brand value was estimated at ₹90,038 crore (US$11 billion).[14] According to the BCCI, the 2015 IPL season contributed ₹1,150 crore (US$140 million) to India's GDP.[15] In December 2022, the IPL achieved a valuation of US$10.9 billion, becoming a decacorn and registering a 75% growth in dollar terms since 2020 when it was valued at $6.2 billion, according to a report by the consulting firm D and P Advisory.[16] Its 2023 final became the most streamed live event on the internet, with 32 million viewers.[17]"""

def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    # print(stopwords)

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    # print(doc)
    tokens = [token.text for token in doc]
    # print(tokens)

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    # print(word_freq)

    max_freq = max(word_freq.values())
    # print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq


    # print(word_freq)


    sent_tokens =[sent for sent in doc.sents]

    print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent :
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else :
                    sent_scores[sent]+= word_freq[word.text]

    # print(sent_scores) 

    select_len = int(len(sent_tokens) * 0.3)   
    # print(select_len)         
    summary = nlargest(select_len,sent_scores,key=sent_scores.get)
    # print(summary)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(text)
    # print(summary)
    # print("length of original text : ",len(text.split(' ')))
    # print("length of summary text : ",len(summary.split(' ')))

    return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))


