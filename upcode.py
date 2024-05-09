#=============================================
#            Flask Server 
#                              #[By Aabit]   
#     Thank  You Upcode Support Team   
#=============================================




from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def load_products_data():
    with open('products.json', 'r', encoding="utf-8") as file:
        return json.load(file)

def save_products_data(data):
    with open('products.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        
        
#...................... GET....................................      
        

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(load_products_data())

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    product = next((p for p in load_products_data() if p['id'] == id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({"Error": "Product Not Found"}), 404
    
 #...................... POST....................................   
   

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    if 'name' not in data or 'price' not in data:
        return jsonify({"Error": "name and price are required"}), 400

    products = load_products_data()
    product = {
        "id": len(products) + 1,
        "Name": data['name'],
        "price": data['price']
    }
    products.append(product)
    save_products_data(products)
    return jsonify(product), 201


#...................... PUT....................................

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    products = load_products_data()
    product = next((p for p in products if p['id'] == id), None)
    if not product:
        return jsonify({"Error": "Product Not found"}), 404
    data = request.json
    product.update(data)
    save_products_data(products)
    return jsonify(product)

#...................... DELETE....................................

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    products = load_products_data()
    products = [p for p in products if p['id'] != id]
    save_products_data(products)
    return jsonify({"message": "Product deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)

