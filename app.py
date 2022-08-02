import streamlit as st
# NLP Pkgs
from textblob import TextBlob
import pandas as pd 
# Emoji
import emoji
# Bar plot
import altair as alt

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Fetch Text From Url
@st.cache
def get_text(raw_url):
	page = urlopen(raw_url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text




def main():
	"""Sentiment Analysis Emoji App """

	st.title("Sentiment Analysis ")

	activities = ["Sentiment","Text Analysis on URL","Text Analysis from Emails"]
	choice = st.sidebar.selectbox("Choice",activities)

	if choice == 'Sentiment':
		st.subheader("Sentiment Analysis")
		st.write(emoji.emojize('Everyone :red_heart: Streamlit ',use_aliases=True))
		raw_text = st.text_area("Enter Your Text","Type Here")
		if st.button("Analyze"):
			blob = TextBlob(raw_text)
			result = blob.sentiment.polarity
			if result > 0.0:
				custom_emoji = ':smile:'
				st.write(emoji.emojize(custom_emoji,use_aliases=True))
			elif result < 0.0:
				custom_emoji = ':disappointed:'
				st.write(emoji.emojize(custom_emoji,use_aliases=True))
			else:
				st.write(emoji.emojize(':expressionless:',use_aliases=True))
			st.info("Polarity Score is:: {}".format(result))
			
	if choice == 'Text Analysis on URL':
		c_sentiment =[]
		st.subheader("Analysis on Text From  Email sample")
		raw_url = st.text_input("Enter URL Here", " ")
		st.write(raw_url)
		text_preview_length = st.slider("Length to Preview",50,100)
		if st.button("Analyze"):
			if raw_url != "Type here":
				result = get_text(raw_url)
				blob = TextBlob(result)
				st.write(blob)
				len_of_full_text = len(result)
				len_of_short_text = round(len(result)/text_preview_length)
				st.success("Length of Full Text::{}".format(len_of_full_text))
				st.success("Length of Short Text::{}".format(len_of_short_text))
				st.info(result[:len_of_short_text])
				c_sentences= blob.split(".")
				for sent in c_sentences:
					blob = TextBlob(sent)
					c_sentiment.append(blob.sentiment.polarity)
				new_df = pd.DataFrame(zip(c_sentences,c_sentiment),columns=['Sentence','Sentiment'])
				st.dataframe(new_df)
				fig = alt.Chart(new_df).mark_bar().encode(x='Sentence',y='Sentiment')
				st.altair_chart(fig,use_container_width=True)

	if choice == 'Text Analysis from Emails':
		c_sentiment =[]
		st.subheader("Analysis on Emails text")
		raw_text = st.text_area("Paste Your Text","  ")
		st.write("Please use: '__##__' as delmeter for each mail")
		
		if st.button("Analyze"):
			if raw_text != "Paste Your Text":
				result = get_text(raw_text)
				blob = TextBlob(result)
				
				c_sentences= blob.split("__##__")
				for sent in c_sentences:
					blob = TextBlob(sent)
					c_sentiment.append(blob.sentiment.polarity)
				new_df = pd.DataFrame(zip(c_sentences,c_sentiment),columns=['Sentence','Sentiment'])
				st.dataframe(new_df)
				fig = alt.Chart(new_df).mark_bar().encode(x='Sentence',y='Sentiment')
				st.altair_chart(fig,use_container_width=True)







if __name__ == '__main__':
	main()