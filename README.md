# Prompt2sql with OpenAI API

##The CSV to SQL Converter is a web application that allows users to upload a CSV file and execute SQL commands on it. It provides a user-friendly interface to interact with CSV data using SQL queries.

Make sure you have the following dependencies installed:

- Python 3.x
- `streamlit`
- `pandas`
- `sqlite3`
- `openai` (Install using `pip install openai`)

You will also need an OpenAI API key. You can sign up for an API key at [OpenAI](https://openai.com/).

## Installation
1. Clone the repository:
2. Install the dependencies:
3. Set up your OpenAI API key: Replace the placeholder `openai.api_key = "YOUR_API_KEY"` with your actual OpenAI API key.

## Usage

1. Run the app:

2. The app will open in your browser. You will see an upload section where you can upload a CSV file.

3. After uploading the file, you can enter an SQL command in the input field and click the "Execute" button.

4. The app will translate the SQL command using the OpenAI API and execute it on the uploaded CSV data. The result will be displayed, and you can choose to visualize it using different chart types.

5. If the SQL command is unclear or missing information, the app will generate a question to clarify. You can provide an example of the natural language query to replace the unclear part.

6. The app keeps a history of executed commands, which you can access in the "History" section. You can select a past command and click the "Execute" button to run it again.


