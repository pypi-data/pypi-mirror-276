import requests
from bs4 import BeautifulSoup
import json

def fetch_conversation_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    data_json = script_tag.string
    data = json.loads(data_json)
    conversation = []

    for message_id, message_data in data['props']['pageProps']['serverResponse']['data']['mapping'].items():
        if 'message' not in message_data:
            continue
        message = message_data['message']
        author_role = message['author']['role']
        if author_role.lower() == 'system':
            continue
        content_type = message['content'].get('content_type', 'text')
        if author_role.lower() == 'user':
            content = " ".join(part if isinstance(part, str) else part.get('text', '') for part in message['content']['parts'])
            conversation.append(("user", content))
        elif author_role.lower() == 'assistant':
            if content_type == 'text':
                content = " ".join(part if isinstance(part, str) else part.get('text', '') for part in message['content']['parts'])
            elif content_type == 'code':
                content = f"```python\n{message['content'].get('text', '')}\n```"
            elif content_type == 'image':
                content = "[Image content not displayable]"
            else:
                continue
            conversation.append(("assistant", content))
    return conversation[::-1]


def create_gpt_colab_notebook(conversations, output_filename, documents):
    cells = []
    num_queries = sum(1 for role, _ in conversations if role == 'user')
    title = "MULTI-TURN" if num_queries > 1 else "SINGLE-TURN"
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [f"{title}\n"]})
    turn_number = 0
    for role, content in conversations:
        if role == 'user':
            turn_number += 1
            query_header = f"Turn {turn_number}\n\nQuery {turn_number}:\n{content}\n\n"
            for idx, link in enumerate(documents, start=1):
                query_header += f"Data {idx}: {link}\n" if len(documents) > 1 else f"Data: {link}\n"
            cells.append({"cell_type": "markdown", "metadata": {}, "source": [query_header]})
        elif role == 'assistant':
            if content.startswith('```python'):
                cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": [content.replace('```python\n', '').replace('\n```', '')]})
            else:
                cells.append({"cell_type": "markdown", "metadata": {}, "source": [content + "\n"]})
    notebook_content = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.8.5", "mimetype": "text/x-python", "codemirror_mode": {"name": "ipython", "version": 3}, "pygments_lexer": "ipython3", "nbconvert_exporter": "python", "file_extension": ".py"}
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(notebook_content, file, ensure_ascii=False, indent=2)

def process_gpt_conversation():
    conversation_url = input("Enter the conversation URL: ")
    rater_id = input("Enter the rater's ID: ")
    row_id = input("Enter the row ID: ")
    num_documents = int(input("Enter the number of documents used: "))
    documents = []
    for i in range(num_documents):
        document_link = input(f"Enter link for Document {i+1}: ")
        documents.append(document_link)
    output_file = f"GPT_rater_{rater_id}_ID_{row_id}.ipynb"
    conversation_data = fetch_conversation_data(conversation_url)
    create_gpt_colab_notebook(conversation_data, output_file, documents)
    print(f"Notebook {output_file} has been created successfully.")