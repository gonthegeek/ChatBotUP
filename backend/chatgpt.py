import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

def create_chain():
    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = TextLoader("data/data.txt")  # Use this line if you only need data.txt
        # loader = DirectoryLoader("data/")
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    return chain

chat_chain = create_chain()

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    query = data.get('question')

    if query in ['quit', 'q', 'exit']:
        return jsonify({'response': 'Goodbye!'})

    result = chat_chain({"question": query, "chat_history": chat_history})
    answer = result['answer']

    chat_history.append((query, answer))

    return jsonify({'response': answer})

if __name__ == '__main__':
    chat_history = []
    app.run(debug=True)
