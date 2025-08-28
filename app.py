# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import PromptTemplate
# from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
# from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Make sure you have a .env file with HUGGINGFACEHUB_API_TOKEN="your_token"

# app = Flask(__name__)
# # Allow requests from any origin for local development.
# CORS(app)


# # --- LangChain Setup ---
# try:
#     embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en")
    
#     llm = HuggingFaceEndpoint(
#         repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
#         task="text-generation",
#         max_new_tokens=512,
#         do_sample=False,
#         temperature=0.1,
#         repetition_penalty=1.03,
#     )
#     model = ChatHuggingFace(llm=llm)

#     prompt_template = """
#           You are a helpful assistant designed to answer questions about a YouTube video based on its transcript.
#           Answer the user's question using ONLY the provided transcript context.
#           If the information is not in the context, explicitly say "I cannot find information about that in the video transcript." Do not make up information.
          
#           Context from the transcript:
#           {context}
          
#           Question: {question}
          
#           Answer:
#     """
#     prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])

# except Exception as e:
#     print(f"Error initializing LangChain components: {e}")
#     embedding_model = None
#     model = None
#     prompt = None


# def get_transcript(video_id):
#     """Fetches and returns the transcript for a given YouTube video ID."""
#     try:
#         ytt_api = YouTubeTranscriptApi()
#         fetched = ytt_api.fetch(video_id, languages=["en"])
#         raw_transcript = fetched.to_raw_data()
#         transcript = " ".join(entry["text"] for entry in raw_transcript)
#         return transcript, None
#     except (TranscriptsDisabled, NoTranscriptFound):
#         return None, "Transcripts are disabled or not available in English for this video."
#     except VideoUnavailable:
#         return None, "This video is unavailable."
#     except Exception as e:
#         return None, f"An unexpected error occurred while fetching the transcript: {str(e)}"

# def format_docs(retrieved_docs):
#     """Formats retrieved documents into a single string."""
#     return "\n\n".join(doc.page_content for doc in retrieved_docs)

# @app.route('/ask', methods=['GET', 'POST'])
# def ask_question():
#     """API endpoint to receive a video ID and question, and return an answer."""
    
#     # This block handles the GET request for testing
#     if request.method == 'GET':
#         return jsonify({"status": "success", "message": "API endpoint is running. Use POST to ask a question."})

#     # The rest of the function handles the POST request from your extension
#     if not model or not embedding_model or not prompt:
#         return jsonify({"error": "Backend models are not initialized."}), 500

#     data = request.get_json()
#     video_id = data.get('video_id')
#     question = data.get('question')

#     if not video_id or not question:
#         return jsonify({"error": "Missing 'video_id' or 'question' in request."}), 400

#     transcript, error = get_transcript(video_id)
#     if error:
#         return jsonify({"error": error}), 404

#     try:
#         splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         chunks = splitter.create_documents([transcript])
#         vector_store = FAISS.from_documents(chunks, embedding_model)
#         retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
#     except Exception as e:
#         return jsonify({"error": f"Failed to create vector store: {e}"}), 500

#     try:
#         rag_chain = (
#             {"context": retriever | format_docs, "question": RunnablePassthrough()}
#             | prompt
#             | model
#             | StrOutputParser()
#         )
#         answer = rag_chain.invoke(question)
#         return jsonify({"answer": answer})
#     except Exception as e:
#         return jsonify({"error": f"Error during question answering: {e}"}), 500

# if __name__ == '__main__':
#     # Explicitly set the port to 5000 to match the extension
#     app.run(debug=True, port=5000)
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
# Make sure to import NoTranscriptFound
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Make sure you have a .env file with HUGGINGFACEHUB_API_TOKEN="your_token"

app = Flask(__name__)
# Allow requests from any origin for local development.
CORS(app)


# --- LangChain Setup ---
try:
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en")
    
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        task="text-generation",
        do_sample=False,
        temperature=0.1,
        repetition_penalty=1.03,
    )
    model = ChatHuggingFace(llm=llm)

    prompt_template = """
          You are a helpful assistant designed to answer questions about a YouTube video based on its transcript.
          Answer the user's question using ONLY the provided transcript context.
          If the information is not in the context, explicitly say "I cannot find information about that in the video transcript." Do not make up information.
          
          Context from the transcript:
          {context}
          
          Question: {question}
          
          Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])

except Exception as e:
    print(f"Error initializing LangChain components: {e}")
    embedding_model = None
    model = None
    prompt = None


# --- UPDATED FUNCTION FOR HINDI & ENGLISH ---
def get_transcript(video_id):
    """Fetches and returns the transcript for a given YouTube video ID.
       It first tries to get the Hindi transcript, and falls back to English if Hindi is not available.
    """
    try:
        # First, try to fetch the Hindi transcript.
        #    ytt_api = YouTubeTranscriptApi()
#         fetched = ytt_api.fetch(video_id, languages=["en"])
#         raw_transcript = fetched.to_raw_data()
#         transcript = " ".join(entry["text"] for entry in raw_transcript)
#         return transcript, None
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["hi"])
        raw_transcript = transcript_list.to_raw_data()
        # print(f"Found Hindi transcript for video ID: {video_id}")
    except NoTranscriptFound:
        try:
            # If Hindi is not found, fall back to English.
            transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
            raw_transcript = transcript_list.to_raw_data()
            # print(f"Hindi not found. Found English transcript for video ID: {video_id}")
        except NoTranscriptFound:
            # If neither is found, return an error.
            return None, "No transcript available in Hindi or English for this video."
    except (TranscriptsDisabled, VideoUnavailable) as e:
        # Handle other potential errors like disabled transcripts or unavailable videos.
        return None, str(e)
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

    # If successful, join the text and return it.
    transcript = " ".join(entry["text"] for entry in raw_transcript)
    return transcript, None
# --- END OF UPDATED FUNCTION ---


def format_docs(retrieved_docs):
    """Formats retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in retrieved_docs)

@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
    """API endpoint to receive a video ID and question, and return an answer."""
    
    if request.method == 'GET':
        return jsonify({"status": "success", "message": "API endpoint is running. Use POST to ask a question."})

    if not model or not embedding_model or not prompt:
        return jsonify({"error": "Backend models are not initialized."}), 500

    data = request.get_json()
    video_id = data.get('video_id')
    question = data.get('question')

    if not video_id or not question:
        return jsonify({"error": "Missing 'video_id' or 'question' in request."}), 400

    transcript, error = get_transcript(video_id)
    if error:
        return jsonify({"error": error}), 404

    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents([transcript])

        if not chunks:
            return jsonify({"error": "The video transcript is too short or empty to be analyzed."}), 400

        vector_store = FAISS.from_documents(chunks, embedding_model)
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        
    except Exception as e:
        print(f"Error during vector store creation: {e}")
        return jsonify({"error": f"Failed to create vector store: {e}"}), 500

    try:
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        answer = rag_chain.invoke(question)
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error during RAG chain invocation: {e}")
        return jsonify({"error": f"Error during question answering: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
