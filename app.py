#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, flash, redirect, request, render_template, jsonify
import numpy as np

from IPython.display import display
from IPython.display import Markdown

import PIL.Image
import textwrap

import os
from werkzeug.utils import secure_filename


# **Gemini model**

# In[2]:


"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import google.generativeai as genai

genai.configure(api_key="AIzaSyCoiYrVdu4T_RQiFBHJwLjt6J8LSbSZowA")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

chatmodel = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

i2t_model = genai.GenerativeModel(model_name="gemini-pro-vision")

convo = chatmodel.start_chat(history=[])
#convo.send_message("hi")
#print(convo.last.text)


# In[ ]:


app = Flask(__name__)

UPLOAD_FOLDER = "image upload/"

app.secret_key="pixelprodigies"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS =set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1) [1].lower() in ALLOWED_EXTENSIONS



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot")
def openchatbot():
    # Render the chatbot template on the chatbot route
    return render_template("chatbot.html")

@app.route("/404", methods=["GET", "POST"])
def page_not_found():
    chatbot_response = None
    if request.method == "POST":
        # Get the user input from the form
        user_query = request.form.get("query", "")
        # Send the user query to the chatbot and get the response
        response = chatmodel.send_message(user_query)
        chatbot_response = response.text
    # Render the 404.html page with the chatbot response
    return render_template("404.html", chatbot_response=chatbot_response)

@app.route("/chat", methods=["POST"])
def query():
    # Handle chat queries here and return appropriate responses
    # You may use the chatbot logic to process user queries
    user_query = request.form.get("user_query")
    # Example chatbot response
    chat_response = "This is a sample response from the chatbot."
    return render_template("404.html", chat_content=chat_response)

@app.route("/img2txt", methods = ["POST"])
def img2text():
    if "file" not in request.files:
        return jsonify({"error":"media not provided"}),400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error":"no file selected"}),400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        img = PIL.Image.open(filename)
        response = i2t_model.generate_content(img)
        return render_template('img2text.html', text_result=response.text)
    else:
        return jsonify({"error":'Allowed image types are - png, jpg, jpeg, gif'}),400


if __name__ == "__main__":
    app.run(port=8000)


# In[ ]:




