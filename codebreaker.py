import google.generativeai as palm
import streamlit as st 

palm.configure(api_key = "AIzaSyAKEaaM7fWIErN3VbikjP_T5m0UfhBy5iE")
models = [m for m in palm.list_models() 
          if 'generateText' 
          in m.supported_generation_methods]
model_bison = models[0]
from google.api_core import retry
@retry.Retry()
def generate_text(prompt,
                  model=model_bison,
                  temperature=0.0):
    return palm.generate_text(prompt=prompt,
                              model=model,
                              temperature=temperature)

def main():
    st.title("Code Explainer by Josh@I")
    
    task_list = ["Write","Explain","Debug","Documentation","Recommend"]
    task = st.selectbox("What is your task",task_list)
    input = st.text_area("ask your question")
    if st.button("Submit"):
           with st.spinner("processing"):
                
                if task == "Write":
                    st.subheader("The most pythonic way to do it is shown below")
                    prompt_template = """
                    {priming}

                    {question}

                    {decorator}

                    Your solution:
                    """
                    priming_text = "You are an expert at writing clear, concise, Python code."
                    decorator = "Insert comments for each line of code."
                    completion = generate_text(prompt = prompt_template.format(priming=priming_text,
                         question=input,
                         decorator=decorator))
                    output = completion.result
                    st.markdown(output)

                if task == "Explain":
                    st.subheader("Demystify the code!")
                    prompt_template = """
                    Can you please explain how this code works?
                    {question}
                    Use a lot of detail and make it as clear as possible.
                    """
                    completion = generate_text(prompt = prompt_template.format(question=input))
                    output = completion.result
                    st.markdown(output)

                if task == "Debug":
                    st.subheader("The Debugger mode is activated")
                    prompt_template = """
                    Can you please help me to debug this code?

                    {question}

                    Explain in detail what you found and why it was a bug.
                    """
                    completion = generate_text(prompt = prompt_template.format(question=input),
                                               temperature=0.5)
                    output = completion.result
                    st.markdown(output)

                if task == "Documentation":
                    st.subheader("Lets write up the documnet")
                    prompt_template = """
                    Please write technical documentation for this code and \n
                    make it easy for a non developer to understand:

                    {question}

                    Output the results in markdown
                    """
                    completion = generate_text(prompt = prompt_template.format(question=input))
                    output = completion.result
                    st.markdown(output)

                if task == "Recommend":
                    st.subheader("Explore multiple ways to code and find the pythonic way!")
                    prompt_template = """
                    I don't think this code is the best way to do it in Python, can you help me?

                    {question}

                    Please explore multiple ways of solving the problem, 
                    and tell me which is the most Pythonic
                    """
                    completion = generate_text(prompt = prompt_template.format(question=input),
                                               temperature=0.3)
                    output = completion.result
                    st.markdown(output)                    






# Run the app
if __name__ == '__main__':
     main()