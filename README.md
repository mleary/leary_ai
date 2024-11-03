# leary_ai

## Overview
I am developing a personal AI chatbot assistant and general GenAI playground for my family. The goal is to explore fun ways to use Gen AI with practical tools that my wife and I can use day to day. There is a large learning component for myself; otherwise this would be overkill compared using existing paid services.

## Main features
* Personalized AI chatbot assistant - I am using Anthropic and Azure OpenAI to create a chatbot that we can use and have more control over than an existing service. I've implemented some basic personalized configuration and will work to potentially fine tune a model for us.

* Fun things for my daughters - My daughters and I like to do "prompt engineering" after building out some basic tools to create images and stories with Gen AI. I moved them to this app to better log the outputs (I now save the images they generate to an Azure Blob Storage container) and allow my wife, who doesn't code, to use them as well.

* A calendar feature - I am working on a calendar feature that will allow us to take pictures of daycare/school calendars and have the app parse them and add them to our shared calendar. Likewise, I would like to be able to ask question and "chat with our shared calendar" with questions like "When are some good times to meet with Dustin for coffee in the morn in the next three weeks?"

    This is a work in progress.

## Future Work
- I am tracking progress and future ideas [here](https://github.com/users/mleary/projects/4).


## Local Setup
This is a Streamlit app that I am hosting in Azure via an App Service. To run locally, you will need to:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/leary_ai.git
    cd leary_ai
    ```

2. **Create and Activate a Virtual Environment**:

  * I am developing this on macOS with Python version 3.12.2


    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  
    # `.venv\Scripts\activate` # for Windows
    ```

3. **Install the Required Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` File**:
    Add the following environment variables to a `.env` file. Note, I recently moved to using Azure OpenAI instead of OpenAI directly, so I am not currently using OpenAI but might in the future. You can see more details on the environment variables [here](### Environment Variables Description), with docs generated by Copilot.

    ```plaintext
    ANTHROPIC_KEY=your_anthropic_api_key_here
    OPENAI_KEY=your_openai_api_key_here
    AZURE_OPENAI_ENDPOINT=https://your-azure-openai-endpoint.com
    AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
    USERNAMES=user1,user2,user3
    EMAILS=user1@example.com,user2@example.com,user3@example.com
    HASHED_PASSWORDS=hashed_password1,hashed_password2,hashed_password3
    AZURE_CONTAINER_NAME=your_container_name_here
    AZURE_CONTAINER_CONNECTION_STRING=your_azure_connection_string_here
    ```
5. **Run the Streamlit App**:
    ```bash
    streamlit run app.py
    ```

6. **Open the App**:
    Open your browser and go to `http://localhost:8501` to view the app.


## Deployment
I choose to host this app in Azure using an App Service. I followed some boilerplate Microsoft instructions to do this, and plan to update this section with more details in the future. Currently, in this repo there are a few files tied to an Azure deployment:

* `.github/workflows/main_learyfamilyai.yml` - This is a GitHub workflow that builds and deploys the app to Azure when changes are made to the `main` branch.
* `startup.sh` - This is a shell script that is run when the app is deployed to Azure. It sets up the environment variables and runs the Streamlit app.
* The environment variables are set in the Azure App Service configuration as well (I did this manually)


### Environment Variables Description

1. **ANTHROPIC_KEY**
    - **Description**: The API key for accessing Anthropic's services.
    - **Example**: `ANTHROPIC_KEY=your_anthropic_api_key_here`

2. **OPENAI_KEY**
    - **Description**: The API key for accessing OpenAI's services.
    - **Example**: `OPENAI_KEY=your_openai_api_key_here`

3. **AZURE_OPENAI_ENDPOINT**
    - **Description**: The endpoint URL for accessing Azure OpenAI services.
    - **Example**: `AZURE_OPENAI_ENDPOINT=https://your-azure-openai-endpoint.com`

4. **AZURE_OPENAI_API_KEY**
    - **Description**: The API key for accessing Azure OpenAI services.
    - **Example**: `AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here`

5. **USERNAMES**
    - **Description**: A comma-separated list of usernames for accessing the application.
    - **Example**: `USERNAMES=user1,user2,user3`

6. **EMAILS**
    - **Description**: A comma-separated list of emails corresponding to the usernames.
    - **Example**: `EMAILS=user1@example.com,user2@example.com,user3@example.com`

7. **HASHED_PASSWORDS**
    - **Description**: A comma-separated list of hashed passwords corresponding to the usernames.
    - **Example**: `HASHED_PASSWORDS=hashed_password1,hashed_password2,hashed_password3`
    - **Note**: You can use the `password_hash.py` file to create hashed passwords.

8. **AZURE_CONTAINER_NAME**
    - **Description**: The name of the Azure Blob Storage container where images will be stored.
    - **Example**: `AZURE_CONTAINER_NAME=your_container_name_here`

9. **AZURE_CONTAINER_CONNECTION_STRING**
    - **Description**: The connection string for accessing the Azure Blob Storage account.
    - **Example**: `AZURE_CONTAINER_CONNECTION_STRING=your_azure_connection_string_here`


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more info.