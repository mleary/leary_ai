# leary_ai
## overview
This is for exploring a personal chatbot assistant for my family.  The goal is to explore fun ways to use Gen AI with practical tools that my wife and I can use day to day. 

## future work

- TBD


## deployment

There is a github workflow setup to kick off a build and release process to Azure when PRs go to `main` branch. It ignores changes to README and other files not tied to dev work.

## setup
This is a streamlit app that I am hosting in Azure via an app service.  to run locally, you will need to:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/leary_ai.git
    cd leary_ai
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add the following items. Note, I recenly moved to using Azure OpenAI versus OpenAI directly, so I am not currently using OpenAI but might in the future. Likewise, I plan to incorporate Anthropic LLMs into this app but haven't yet.

    
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

### Environment Variables Description

1. **ANTHROPIC_KEY**
    - **Description**: The API key for accessing Anthropic's services.
    - **Example**: `ANTHROPIC_KEY=your_anthropic_api_key_here`

2. **OPENAI_KEY**
    - **Description**: The API key for accessing OpenAI's services.
    -**Example**:`OPENAI_KEY=your_openai_api_key_here`

3. **AZURE_OPENAI_ENDPOINT**
    - **Description**: The endpoint URL for accessing Azure OpenAI services.
    - **Example**:`AZURE_OPENAI_ENDPOINT=https://your-azure-openai-endpoint.com`

4. **AZURE_OPENAI_API_KEY**
    - **Description**: The API key for accessing Azure OpenAI services.
    - **Example**:`AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here`

5. **USERNAMES**
    - **Description**: A comma-separated list of usernames for accessing the application.
    - **Example**: `USERNAMES=user1,user2,user3`

6. **EMAILS**
    - **Description**: A comma-separated list of emails corresponding to the usernames.
    -**Example**:`EMAILS=user1@example.com,user2@example.com,user3@example.com`

7. **HASHED_PASSWORDS**
    - **Description**: A comma-separated list of hashed passwords corresponding to the usernames.
    -**Example**:`HASHED_PASSWORDS=hashed_password1,hashed_password2,hashed_password3`
    -**Note:** You can use the `password_hash.py` file to create hashed passwords

8. **AZURE_CONTAINER_NAME**
    - **Description**: The name of the Azure Blob Storage container where images will be stored.
    -**Example**:`AZURE_CONTAINER_NAME=your_container_name_here`

9. **AZURE_CONTAINER_CONNECTION_STRING**
    - **Description**: The connection string for accessing the Azure Blob Storage account.
    -**Example**:`AZURE_CONTAINER_CONNECTION_STRING=your_azure_connection_string_here`


5. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

6. Open your browser and go to `http://localhost:8501` to view the app.
