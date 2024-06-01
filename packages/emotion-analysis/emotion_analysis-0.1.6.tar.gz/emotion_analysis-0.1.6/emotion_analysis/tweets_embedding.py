import os
import numpy as np
from transformers import (
    RobertaTokenizer,
    RobertaModel,
    BertModel,
    BertTokenizer,
)
import torch


# Get the current directory where this script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the directory of this script
os.chdir(current_directory)

# Define the functions for extracting vector representations

print("TWEETS EMBEDDING BERT AND ROBERTA IMPORT START!")


def get_vector_bert(text, model_name="bert-base-uncased"):
    """
    Get vector representation of text using BERT.

    Parameters:
    - text (str): The input text.
    - model_name (str): The pre-trained BERT model to use.

    Returns:
    - list: The embedding vector.
    """
    # Load pre-trained BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)

    # Forward pass through BERT model
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract the embeddings for [CLS] token (the first token)
    cls_embedding = outputs.last_hidden_state[:, 0, :]

    # Convert tensor to list
    cls_embedding_list = cls_embedding.squeeze().tolist()

    return cls_embedding_list


def get_vector_roberta(
    text,
    model_name="roberta-base",
):
    """
    Get vector representation of text using RoBERTa.

    Parameters:
    - text (str): The input text.
    - model_name (str): The pre-trained RoBERTa model to use.

    Returns:
    - np.ndarray: The embedding vector.
    """
    try:

        tokenizer = RobertaTokenizer.from_pretrained(model_name)
        model = RobertaModel.from_pretrained(model_name)
        inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        cls_embedding_list = cls_embedding.squeeze().numpy()
        return cls_embedding_list
    except Exception as e:
        print(f"Error in get_vector_roberta: {e}")
        return np.zeros(768)


print("TWEETS EMBEDDING BERT AND ROBERTA IMPORT SUCCESSFUL!")
