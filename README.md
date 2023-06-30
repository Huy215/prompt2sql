# prompt2sql
The CSV to SQL Converter is a web application that allows users to upload a CSV file and execute SQL commands on it. It provides a user-friendly interface to interact with CSV data using SQL queries.

Install the required dependencies:
  pip install streamlit
  pip install streamlit_option_menu
  pip install openai
  pip install pandas
  pip install sqlite3

Set up the OpenAI API credentials:
  Obtain an API key from OpenAI.
  Open the app.py file and replace the empty string "" with your OpenAI API key: openai.api_key = "<your_api_key>"

Run the application: streamlit run prompt2sql.py
