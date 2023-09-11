from flask import Flask, request, jsonify
import MySQLdb

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = '*****'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '******'  
app.config['MYSQL_DB'] = 'stock_db'

mysql = MySQLdb.connect(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])

@app.route('/dialogflow-webhook', methods=['POST'])
def dialogflow_webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req['queryResult']['intent']['displayName']

    if intent_name == 'equity':
        company_name = req['queryResult']['parameters']['stock-names']
        response_text = fetch_price_to_equity(company_name)
    elif intent_name == 'market.cap':
        company_name = req['queryResult']['parameters']['stock-names']
        response_text = fetch_market_cap(company_name)
    else:
        response_text = "This intent is not handled by the webhook."

    return jsonify({
        "fulfillmentText": response_text
    })

def fetch_price_to_equity(company_name):
    cursor = mysql.cursor()
    query = "SELECT price_to_equity FROM stock_data WHERE company_name = %s"
    cursor.execute(query, (company_name,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return f"The Price to Equity of {company_name} is {result[0]}."


    else:
        return f"Sorry, I couldn't find the Price to Equity for {company_name}."

def fetch_market_cap(company_name):
    cursor = mysql.cursor()
    query = "SELECT market_capitalisation FROM stock_data WHERE company_name = %s"
    cursor.execute(query, (company_name,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return f"The Market Capitalisation of {company_name} is {result[0]}."

    else:
        return f"Sorry, I couldn't find the Market Capitalisation for {company_name}."

if __name__ == '__main__':
    app.run(debug=True)
