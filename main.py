from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import psycopg2
 
 ### Dont call the api at / endpoint as the postgres connection is still under construction


app = Flask(__name__)

details_data = {}
diary_data = []



def get_phq_severity(score):
    if score < 5:
        return "Minimal severity level"
    elif score < 10:
        return "Mild severity level"
    elif score < 15:
        return "Moderate severity level"
    else:
        return "Severe level"

def algo(number):

    phq_dataset = pd.read_csv('./datasets/phq.csv')

    user_phq_dataset = phq_dataset[phq_dataset['Score'] == number]

    phq_features = user_phq_dataset[['Score', 'Gender', 'Age', 'Employment Status', 'Relation Status']]
    phq_target = user_phq_dataset['Score']

    phq_features_encoded = pd.get_dummies(phq_features)

    X_phq_train, X_phq_test, y_phq_train, y_phq_test = train_test_split(phq_features_encoded, phq_target, test_size=0.2, random_state=42)

    phq_model = LinearRegression()

    phq_model.fit(X_phq_train, y_phq_train)

    next_phq_score = int(np.round(phq_model.predict(X_phq_test.iloc[-1:].values)[0]))

    actual_phq_score = y_phq_test.iloc[-1]

    predicted_phq_severity = get_phq_severity(next_phq_score)

    print(f"Predicted next PHQ-9 score for score {number} is:", next_phq_score, predicted_phq_severity)
    print("Actual Next PHQ-9 Score:", actual_phq_score)
    print("Prediction Accuracy (RMSE) for PHQ-9:", np.sqrt(mean_squared_error([actual_phq_score], [next_phq_score])))
    return f'{predicted_phq_severity}'



def create_tables():
    conn = psycopg2.connect(
        dbname="'postgres'",
        user="postgres",
        password="postgres",
        host="192.168.1.6",      # put your system ip
        port="5435"
)
    cursor = conn.cursor()
    
    create_user_table_query = """
        CREATE TABLE IF NOT EXISTS user (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            password VARCHAR(100)
        );
    """
    
    create_mst_dates_table_query = """
        CREATE TABLE IF NOT EXISTS mst_dates (
            id SERIAL PRIMARY KEY,
            notdate DATE UNIQUE
        );
    """
    
    create_result_table_query = """
        CREATE TABLE IF NOT EXISTS result (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES user(id),
            gad_result INT,
            phq_result INT
        );
    """
    
    create_journal_table_query = """
        CREATE TABLE IF NOT EXISTS journal (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES user(id),
            mst_dates_id INT REFERENCES mst_dates(id),
            text VARCHAR(200)
        );
    """
    
    cursor.execute(create_user_table_query)
    cursor.execute(create_mst_dates_table_query)
    cursor.execute(create_result_table_query)
    cursor.execute(create_journal_table_query)
    
    conn.commit()


@app.route('/',methods=['GET'])
def hello():

    create_tables()
    return "hello World"

@app.route('/userdetail', methods=['POST'])
def user_detail():
    data = request.get_json()

    username = data['username']
    password = data['password']
    insert_user_query = """
        INSERT INTO user (name, password) VALUES (%s, %s) RETURNING id;
    """
    with conn.cursor() as cursor:
        cursor.execute(insert_user_query, (username, password))
        user_id = cursor.fetchone()[0] 
        conn.commit()
        
    return jsonify({'user_id': user_id}), 200

 ####       /getphq recieves data in json format : {"value":<number>}

@app.route('/getphq', methods=['POST'])
def get_phq():
    data = request.get_json()
    value = data['value']
    getresult = algo(int(value))
    return jsonify({'message': 'Details added successfully', "result": getresult})


 ####       /getgad recieves data in json format : {"value":<number>}

@app.route('/getgad', methods=['POST'])
def get_gad():
    data = request.get_json()
    value = data['value']
    getresult = algo(int(value))
    return jsonify({'message': 'Details added successfully',"result":getresult})



@app.route('/diary', methods=['POST'])
def add_diary_entry():
    data = request.get_json()
   
    return jsonify({'message': 'Diary entry added successfully'})



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


## My system ip 192.168.1.6
    
