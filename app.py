import os
import shutil
import streamlit as st
from PIL import Image
from lyzr import ChatBot

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

# Set Streamlit page configuration
st.set_page_config(
    page_title="Lyzr",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Enhanced Movie Search 🔍")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown("Welcome to the Enhanced Movie Search app! Describe your movie preferences, and we'll recommend the most relevant films based on your criteria.")




# Function to remove existing files in the directory
def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")

# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)

# Function to implement RAG Lyzr Chatbot
def rag_implementation(file_path):
    _, file_extension = os.path.splitext(file_path)
    supported_extensions = [".pdf", ".docx"]

    if file_extension.lower() in supported_extensions:
        model = "gpt-4-turbo-preview"
        if file_extension.lower() == ".pdf":
            return ChatBot.pdf_chat(input_files=[file_path], llm_params={"model": model})
        else:
            return ChatBot.docx_chat(input_files=[file_path], llm_params={"model": model})
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX files are supported.")

# Function to get Lyzr response
def advisor_response(file_path, search_query):
    rag = rag_implementation(file_path)
    prompt = f""" 
You are an Expert MOVIE ANALYST and RECOMMENDER. Your task is to THOROUGHLY ANALYZE a PDF file that lists various movies and SUGGEST the most relevant films to a user based on their preferences provided in a search query. 

To accomplish this task, follow these steps:

1. EXAMINE the PDF file {file_path} carefully to UNDERSTAND the scope of movies available within it.

2. IDENTIFY key details {search_query}for each movie such as genre, ratings from recognized platforms (like IMDb), specific tags that categorize the movie's themes or content, director names, and notable actors.

3. FILTER the list by each of the user's preferences in the search query to NARROW DOWN potential recommendations. If the user provides information about any one of these fields—genre, tags, actors/actresses, director, or language {search_query use that information to match and recommend relevant movies from the uploaded file.

4. COMPARE movies within the filtered results to DETERMINE which ones stand out based on overall critical acclaim and relevance to the user's interests.

5. SELECT a variety of movies that BEST MATCH all or most of the given preferences to provide a diverse set of recommendations.

6. PREPARE a personalized list of recommended movies for the user with a brief explanation in one sentence as to why each film was chosen based on their specified criteria. Make sure if there are NO MATCHES for a given set of preferences, DO only display a courteous message informing them: "Sorry, we couldn't find any movies that match your specific criteria". Just Display this message alone and nothing else.

You MUST ensure that your recommendations are as ACCURATE and TAILORED as possible to deliver an EXCEPTIONAL movie recommendation experience.


"""
    prompt += f"\nUser's preferences: {search_query}"
    response = rag.chat(prompt)
    return response.response

# File path to the movie data
file_path = "list_movies.pdf"

# Check if file path is not empty and exists
if file_path and os.path.exists(file_path):
     
    # User input 
    search_query = st.text_input("Describe your movie preferences:")

    # Generate advice button
    if st.button("Search"):
        if not search_query:
            st.warning("Please enter your movie preferences.")
        else:
            recommendations = advisor_response(file_path, search_query)
            st.markdown(recommendations)
else:
    st.info("Please enter a valid file path.")

# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """Experience the seamless integration of Lyzr's ChatBot as you refine your documents with ease. For any inquiries or issues, please contact Lyzr."""
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )
