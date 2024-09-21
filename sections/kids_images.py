import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
from PIL import Image
import requests
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def dalle_image(user_prompt):
    """
    Generates an image using the DALL-E model based on the given user prompt.

    Args:
        user_prompt (str): The prompt provided by the user.

    Returns:
        str: The URL of the generated image.
    """
        # Set up the Azure OpenAI client
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
        api_version="2024-07-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"))

    id =  datetime.now().strftime("%Y%m%d%H%M%S")
    response = client.images.generate(
        model="dall-e-3",
        prompt=user_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url, user_prompt, id


def save_image_to_azure(url, container_name, blob_name, connection_string, metadata=None):

    """
    Downloads an image from the given URL and uploads it to Azure Blob Storage with metadata.

    Args:
        url (str): The URL of the image to download.
        container_name (str): The name of the Azure Blob Storage container.
        blob_name (str): The name of the blob to create in the container.
        connection_string (str): The connection string to the Azure Blob Storage account.
        metadata (dict, optional): Metadata to associate with the blob.

    Returns:
        str: The URL of the uploaded image in Azure Blob Storage.
    """
    # Download the image
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download image from {url}")

    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get a container client
    container_client = blob_service_client.get_container_client(container_name)

    # Create the container if it does not exist
    try:
        container_client.create_container()
    except Exception as e:
        pass  # Container already exists

    # Get a blob client
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the image to Azure Blob Storage with metadata
    blob_client.upload_blob(BytesIO(response.content), overwrite=True, metadata=metadata)

    # Return the URL of the uploaded image
    blob_url = blob_client.url
    return blob_url


def render():
    st.header("🖼️ Image generator")
    
    # Create a dropdown selection
    # Create two columns
    col1, col2 = st.columns(2)

    # Place the dropdown selection in the first column
    with col1:
        creator = st.multiselect(
            'Creator', ('Nora', 'Tess', 'Matt', 'Ann-Marie', 'Someone else!'))

    # Place the multiselect in the second column
    with col2:
        type = st.selectbox(
            'What type of image?', ["cartoon", "realistic image"], index=0)

    user_input = st.text_input("Describe your image here:")

    # Create a button
    if st.button('Create'):
        # Print request & create a placeholder
        placeholder = st.empty()
        placeholder.text('Creating an image based on your input...')
        prompt = user_input + "The image should be a " + type
        image_url, prompt, id = dalle_image(prompt)
        placeholder.text('Downloading picture for display...')
        # generate metadata
        metadata = {
        "id":id,
        "author": ", ".join(creator),
        "prompt": prompt,
        'tags': ", ".join(type)
        }

        save_image_to_azure(
            url = image_url, 
            container_name = os.getenv("AZURE_CONTAINER_NAME"), 
            blob_name=f'{id}.jpg',
            connection_string = os.getenv("AZURE_CONTAINER_CONNECTION_STRING"),
            metadata=metadata)
        if image_url:
            try:
                # Fetch the image from the URL
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))

                # Display the image
                st.image(image, caption="Image info:", use_column_width=True)
                st.markdown(f"Prompt: {prompt}<br>[View Image]({blob_url})", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
            