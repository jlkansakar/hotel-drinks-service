import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import swag_from
from swagger.config import init_swagger

app = Flask(__name__)
init_swagger(app)
CORS(app)

@app.route("/")
@swag_from("swagger/home.yaml")
def home():
    return jsonify({
        "service": "Drinks service",
        "version": "1.0.0",
        "description": "A RESTful API service that provides drinks",
    })

@app.route("/api")
@swag_from("swagger/api.yaml")
def api(): 
    return jsonify({
        "home": "https://drinks-service-fvf5eph2g3gybfhq.northeurope-01.azurewebsites.net",
        "api": "https://drinks-service-fvf5eph2g3gybfhq.northeurope-01.azurewebsites.net/api",
        "drinks list": "https://drinks-service-fvf5eph2g3gybfhq.northeurope-01.azurewebsites.net/drinks",
        "specific drink by id": "https://drinks-service-fvf5eph2g3gybfhq.northeurope-01.azurewebsites.net/drinks/<int:drink_id>",
        "openAPI documentation": "https://editor.swagger.io/whatever-the-link-is-when-actually-made"
    })




@app.route("/drinks", methods=['GET', 'POST'])
@swag_from("swagger/drinks.yaml")
def drinks():
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM drinks')
        result = cursor.fetchall()

        if not result:
            return jsonify([])

        drinks = []

        for row in result:
            drink = {
                "drink_id": row[0],
                "drink_name": row[1],
                "category": row[2],
                "price": row[3],
                "sale_count": row[4]
            }
            drinks.append(drink)

        conn.close()
        
        return jsonify(drinks)
    
    elif request.method == 'POST':
        data = request.get_json()
        drink_name = data.get('drink_name')
        category = data.get('category')
        price = data.get('price')
        sale_count = data.get('sale_count')

        cursor.execute('''
            INSERT INTO guests (drink_name, category, price, sale_count)
            VALUES (?, ?, ?, ?)
        ''', (drink_name, category, price, sale_count))
        
        drink_id = cursor.lastrowid

        conn.commit()
        conn.close()

        new_drink = {
            "drink_id": drink_id,
            "drink_name": drink_name,
            "category": category,
            "price": price,
            "sale_count": sale_count
        }
        
        return jsonify(new_drink), 201
    

@app.route("/drinks/<int:drink_id>", methods=['GET','DELETE', 'PUT', 'PATCH'])
@swag_from("swagger/drinkID.yaml")
def drink(drink_id):
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM drinks WHERE drink_id = ?', (drink_id,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({"error": "Drink not found"}), 404

        
        drink = {
            "drink_id": result[0],
            "drink_name": result[1],
            "category": result[2],
            "price": result[3],
            "sale_count": result[4]
        }

        conn.close()
        
        return jsonify(drink)
    
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM drinks WHERE drink_id = ?', (drink_id,))
        conn.commit()
        conn.close()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Drink not found"}), 404
        
        return "", 204

    elif request.method in ['PUT', 'PATCH']:
        data = request.get_json()
        drink_name = data.get("drink_name")
        category = data.get("category")
        price = data.get("price")
        sale_count = data.get("sale_count")

        cursor.execute('''
            UPDATE drinks
            SET drink_name = COALESCE(?, drink_name), 
                category = COALESCE(?, category), 
                price = COALESCE(?, price),
                sale_count = COALESCE(?, sale_count)
            WHERE drink_id = ?
        ''', (drink_name, category, price, sale_count, drink_id))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Drink not found"}), 404

        conn.close()
        return jsonify({"message": "Drink updated successfully"}), 200
    

if __name__ == "__main__":
    app.run()