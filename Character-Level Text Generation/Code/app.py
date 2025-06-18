import streamlit as st
import nltk
from nltk.corpus import gutenberg

# Download NLTK Gutenberg corpus if not downloaded
nltk.download('gutenberg')

# Prepare books
texts = {}
book_ids = ['austen-emma.txt', 'austen-persuasion.txt', 'shakespeare-hamlet.txt',
            'austen-sense.txt', 'bible-kjv.txt']

for book in book_ids:
    texts[book] = gutenberg.raw(book).lower()


def generate_next_chars_verbatim(text, prompt, length):
    """Extract literal text from original book starting from prompt by character."""
    idx = text.find(prompt)
    if idx == -1:
        return "Input size exceeded limit!"
    return text[idx:idx + len(prompt) + length]


def generate_next_word_verbatim(text, prompt, length):
    """Returns the first full word that starts with the prompt, and the next `length-1` words."""
    words = text.split()
    
    # Find first word that starts with the prompt (not just equal)
    idx = -1
    for i, word in enumerate(words):
        if word.startswith(prompt):
            idx = i
            break

    if idx == -1 or idx + length > len(words):
        return "Prompt not found or too close to end of text."

    return " ".join(words[idx:idx+1 + length])


# Streamlit UI
st.title("Text Generator")
st.sidebar.title("Settings")

# Book selection
selected_book = st.sidebar.selectbox("Select a book", book_ids)

# Generation style
generation_style = st.sidebar.selectbox("Select generation style", ["character", "word"])

# Prompt
prompt = st.text_input("Enter a starting sentence or word:")

# Number of subsequent tokens
length = st.number_input("How many subsequent tokens to extract?", min_value=0, max_value=500, value=5)

if st.button("Generate"):
    if prompt:
        if generation_style == "character":
            result = generate_next_chars_verbatim(texts[selected_book], prompt.lower(), length)
        else:
            result = generate_next_word_verbatim(texts[selected_book], prompt.lower(), length)

        st.text_area("Extracted text", result, height=200)
    else:
        st.error("Please enter a prompt.")
