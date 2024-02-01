import streamlit as st
import tools

import streamlit as st


st.title("🎤 Transform PDF Courses into Engaging Audio Conversations!")

st.write("Upload a PDF course, and get a personalized audio conversation between teacher and student 🚀. Dive into the content with real-world examples, making learning interactive and fun! 🌟")

uploaded_file = st.file_uploader("📤 Upload PDF File", type=["pdf"])


if uploaded_file is not None:
    if st.button("🚀 Convert to Audio"):
        content = tools.extract_text_from_pdf(uploaded_file)
        conversation = tools.start_working(content)
        tools.text_to_audio(conversation)
        st.success("🎉 Audio conversion completed!")
        st.audio("combined_audio.mp3")
        with st.expander("The conversation"):
            st.write(conversation)


