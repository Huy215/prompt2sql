import streamlit as st
from streamlit_option_menu import option_menu
import openai
import pandas as pd
import sqlite3

# Set up the OpenAI API credentials
openai.api_key = "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" #openAI API key

# Define the translate function
def translate(text, arrays_column_names):
    prompt = f"Translate the following natural language query into SQL: \n#{f'data({arrays_column_names})'}###{text}\nSQL command:"
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=["#", ";"],
        temperature=0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    message = completions.choices[0].text.strip()
    return message
#Define the advise funtion
def answer(sql_command,arrays_column_names):
    question_prompt = f"Given data contain column {f'data({arrays_column_names})'}#Given the SQL command convert from natural language: {sql_command}, what information is missing or unclear and give me an example of nature language should I enter to replace. Answer in a simple word ?"
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question_prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    question = completions.choices[0].text.strip()
    return question

# Define a function to execute the SQL command on the CSV data
def execute_sql_command(dataframe, sql_command):
    conn = sqlite3.connect(':memory:')
    dataframe.to_sql('data', conn, index=False, if_exists='replace')
    result = pd.read_sql(sql_command, conn)
    conn.close()
    return result
# Define a function to store all the column names
def store_column_name(dataframe):
    columns = dataframe.columns.tolist()
    column_names = list(dataframe.columns)
    formatted_column_names = ", ".join(column_names)
    return formatted_column_names

#Visualiza data
def visualize_data(dataframe):
    data_option = st.selectbox("Select a visualize chart", ["Line chart", "Bar chart", "Area chart", "Scatter plot"])
    if data_option == "Line chart":
        st.line_chart(dataframe)
    elif data_option == "Bar chart":
        st.bar_chart(dataframe)
    elif data_option == "Area chart":
        st.area_chart(dataframe)
    elif data_option == "Scatter plot":
        st.map(dataframe)

# Set up the app layout
st.set_page_config(page_title='CSV to SQL Converter', page_icon=':file_folder:')
st.title('CSV to SQL Converter')
st.write('Upload a CSV file and execute SQL commands on it.')


# Initialize the past_command list
if 'past_command' not in st.session_state:
    st.session_state.past_command = []
#Contain the uploaded data into memory
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None


# Create a file uploader component
uploaded_file = st.file_uploader('Upload a CSV file', type='csv')
if uploaded_file is not None:
    st.session_state.dataframe = pd.read_csv(uploaded_file)
    st.write('## Data set')

#GUI
selected= option_menu(
    menu_title="Main Menu",
    options=["Projects","History","Download"],
    icons=["house","clock-history","download"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected =="Projects":
    # Create an input field for the SQL command
    sql_command = st.text_input('Enter an SQL command')
    # If the user has uploaded a file, display it and create a DataFrame
    if uploaded_file is not None:
        if sql_command != '':
            st.write('Uploaded file:')
            # Store column names in an array
            store_column_name(st.session_state.dataframe)
            # Translate the SQL command using the translate() function
            translated_command = translate(sql_command, store_column_name(st.session_state.dataframe))
            # Execute the translated SQL command
            st.write(translated_command)
            if translated_command.strip().upper().startswith("SELECT"):
                try:
                    result = execute_sql_command(st.session_state.dataframe, translated_command)
                    try:
                        if [sql_command,result] not in st.session_state.past_command:
                            st.session_state.past_command.append([sql_command,result])
                    except:
                        pass
                    st.write('Result:')
                    st.write(result)
                    # Choose data visualize
                    visualize_data(result)
                except:
                    responded = answer(sql_command,store_column_name(st.session_state.dataframe))
                    st.write(f"AI-generated question: {responded}")
            else:
                conn = sqlite3.connect(':memory:')
                st.session_state.dataframe.to_sql('data', conn, index=False, if_exists='replace')
                cursor = conn.cursor()
                try:
                    cursor.execute(translated_command)
                    conn.commit()
                    st.success('SQL command executed successfully.')
                    # Retrieve the updated DataFrame from the database
                    updated_df = pd.read_sql_query('SELECT * FROM data', conn)    
                    # Display the updated DataFrame
                    st.write(updated_df)
                    save_button=st.button('Save')
                    if save_button:
                        st.session_state.dataframe=updated_df
                        st.success("File saved")
                except sqlite3.Error as e:
                    st.error(f'Error executing SQL command: {e}')
                finally:
                    cursor.close()
                    conn.close()
        else:
            # Store column names in an array
            store_column_name(st.session_state.dataframe)
            st.write(f"data({store_column_name})")
            # Display first 10 rows of the dataframe
            st.write("First 10 rows of the uploaded CSV file:")
            st.write(st.session_state.dataframe.head(10))
    else:
        st.write('Please upload a CSV file')

if selected =="History":
    st.subheader('History')
    st.sidebar.markdown("# Past Command")
    #Input field
    add_command=st.text_input('Enter an SQL commands')

    col1, col2, col3 = st.columns(3)
    
    for i, command in enumerate(st.session_state.past_command):
        if i not in st.session_state:
            st.session_state[i]=False

        if f"past_dataframe_{i}" not in st.session_state:
            st.session_state[f"past_dataframe_{i}"]=None

        if f"page_number_{i}" not in st.session_state:
            st.session_state[f"page_number_{i}"]=1
        
            
        if st.sidebar.button(command[0], key=f"button_{i}") or st.session_state[i]:
            st.session_state[i]=True
            st.session_state[f"past_dataframe_{i}"]=command[st.session_state[f"page_number_{i}"]]
            
            #Navigate through page
            with col2:
                st.write("Page "+str(st.session_state[f"page_number_{i}"])+"/"+str(len(command)-1))
            with col1:
                if st.button("<=", key=f"backward_{i}"):
                    st.session_state[f"page_number_{i}"]-=1
                    if st.session_state[f"page_number_{i}"] < 1:
                        st.session_state[f"page_number_{i}"]=len(command)-1
            with col3:
                if st.button("=>",key=f"forward_{i}"):
                    st.session_state[f"page_number_{i}"]+=1
                    if st.session_state[f"page_number_{i}"]>=len(command):
                        st.session_state[f"page_number_{i}"]=1
            
            if add_command !='':
                store_column_name(st.session_state[f"past_dataframe_{i}"])
                past_translated_command = translate(add_command, store_column_name(st.session_state[f"past_dataframe_{i}"]))
                st.write(past_translated_command)
                past_result=execute_sql_command(st.session_state[f"past_dataframe_{i}"],past_translated_command)
                st.write(past_result)
                visualize_data(past_result)
                command.append(past_result)
                add_command=st.empty()
            else:
                st.write(st.session_state[f"past_dataframe_{i}"])
                visualize_data(st.session_state[f"past_dataframe_{i}"])
                st.write(i)
            clear=st.button("Clear",key=f"clear_{i}")
            ballon=st.button("Ballon",key=f"ballon_{i}")
            if clear:
                st.session_state[i]=False
            if ballon:
                st.balloons
    
if selected =="Download":
    st.write(execute_sql_command(st.session_state.dataframe, 'SELECT * FROM data'))
    st.download_button(label="Download CSV",data=st.session_state.dataframe.to_csv(),file_name="data.csv",mime='text/csv')