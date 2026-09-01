# DEVELOPMENT OF A MULTILINGUAL AI-POWERED INFORMATION AND ADVISORY CHATBOT FOR ISTANBUL SABAHATTIN ZAIM UNIVERSITY

An AI-powered chatbot prototype developed for Istanbul Sabahattin Zaim University (IZU). The system aims to answer users' questions using information obtained from the university's web resources.

## Features

- Question answering about university and academic information
- Access to academic staff information
- Turkish and English language support
- Use of information collected from web resources
- Vector-based information retrieval
- Streamlit-based chatbot interface

## Technologies Used

- Python
- Streamlit
- OpenAI API
- ChromaDB
- HTML/CSS

## System Overview

As part of the project, data is collected from university web resources, processed and divided into chunks, and converted into embeddings. The resulting data is stored in ChromaDB. When a user submits a question, relevant information is retrieved through vector-based search, and the retrieved content is used to generate an AI-powered response.

This project was developed as part of the **BAP-100 Research Project**.

## How to Run


1\. Install required packages:



```bash

pip install -r requirements.txt

