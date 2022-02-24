#Importing Libs
import streamlit as st
import datetime
import pandas as pd
import psycopg2

# --- Intro ---
st.title('First Project Interacting With Database')
st.subheader('Using Streamlit to Insert in Database')

introPart1 = '''
One of the most important parts in a Data product is the Data acquisition, many times this stage is done by Data Collection. This simple Streamlit Web application shows an easy way to do that.'''

st.write(introPart1)

introPart2 ='''
Those are the steps the app will follow: (1)-Access the Database created before and hosted in Heroku,(2)-Insert Data, (3)-Access the Table in Database.'''
st.write(introPart2)

st.info('**DON\'t WORRY**, your Database credentials won\'t be grabbed. You can check this app code in https://github.com/orlandojrps/FirstSql')


# --- PART 1 ---
st.header('Part 1 - Credentials for Database')

HOST = st.text_input("Insert 'Host'")
HOST = HOST.replace(" ", "")
DBNAME = st.text_input("Insert 'Database'")
DBNAME = DBNAME.replace(" ", "")
USER = st.text_input("Insert 'User'")
USER = USER.replace(" ", "")
PORT = st.text_input("Insert 'Port'")
PORT = PORT.replace(" ", "")
PASSWORD = st.text_input("Insert 'Password'")
PASSWORD = PASSWORD.replace(" ", "")


# --- PART 2 ---
st.header('Part 2 - Data Acquisition')
st.markdown('_**Let´s Talk About Politics...**_')

st.image('vote.jpg', caption='Show your opinion! Speak LOUD!')

answer1 = st.select_slider('What is you opinion about your country’s politicians?', options=['Hate','Don’t Like','indifferent','Like', 'Love'], value='indifferent')
answer2 = st.slider('Give a satisfaction value From 0 to 100?', min_value=0, max_value=100)


# --- 2 SQL Functions: most important part of this code
#documentation https://www.psycopg.org/docs/module.html

def interact_sql(query):
    #Goal: Create table or insert data
    conn = psycopg2.connect(dbname=DBNAME,
                            user = USER,
                            password = PASSWORD,
                            host = HOST,
                            port = PORT)   
    cur = conn.cursor()
    cur.execute(query)
    cur.close
    conn.commit()
    conn.close()


def acquire_table(query):
    #Goal: Create table or insert data
    conn = psycopg2.connect(dbname=DBNAME,
                            user = USER,
                            password = PASSWORD,
                            host = HOST,
                            port = PORT)   
    cur = conn.cursor()
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall(), columns=['date','opinion','satisfaction'])
    cur.close
    conn.commit()
    conn.close()
    return df


# --- Saving data  ---
if st.button('Send Data'):

    #criando a tabela sql
    try:
        query1 = '''CREATE TABLE IF NOT EXISTS table_politic(
                    date VARCHAR,
                    opinion VARCHAR,
                    satisfaction INT
                    );
        '''

        interact_sql(query1)
        st.write("Success: table 'table_politic' was created.")
    except:
        st.write("Error: table 'table_politic' was not created.")

    #insert Data into table
    try:
        query2 = f'''INSERT INTO table_politic (date, opinion, satisfaction)
                    VALUES ('{datetime.datetime.now().strftime('%d-%m-%Y')}', '{answer1}', {answer2});
        '''

        interact_sql(query2)

        st.info(f'''**Data sent**:\n
            1) What is you opinion about your country’s politicians? {answer1}\n
            2) Give a satisfaction value From 0 to 100 {answer2}
            ''')
    except:
        st.write('Error: Data could not be inserted.')


    # --- PART 3 ---
st.header('Part 3 - Access SQL table created')

try:
    df = acquire_table('SELECT * FROM table_politic')
    st.write(df)
except:
    st.write('Error: Connection unavaliable.')
