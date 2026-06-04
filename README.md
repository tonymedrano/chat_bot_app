## create environment:

```bash
chabot_env
```

## install dependencies:

```bash
pip install streamlit
pip install openai
pip install streamlit-js-eval
```
## or just run:

```bash
pip install -r ./requirements.txt
```
## run streamlit:

```bash
streamlit run app.py
```
## streamlit code examples:
```python
st.title("Hello, Streamlit!")
st.title('_This_ is :blue[a title] :speech_balloon:')
st.title('$E=mc^2$')
st.header("This is a header")
st.subheader("This is a subheader")
st.text("This is some text.")
st.markdown("This is **bold** text, this is *italic* text, and this is a [link](https://www.streamlit.io).")
st.markdown("This is a list:\n- Item 1\n- Item 2\n- Item 3")
st.write("This is a write message.")
st.success("This is a success message.")
st.warning("This is a warning message.")
st.latex(r'E=mc^2')

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

st.dataframe(data)

st.write(data)
```