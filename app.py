from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Temporary in-memory database mock container array
contacts_db = [
    {
        "id": 1,
        "name": "Johnny Appleseed",
        "phone": "1-800-MY-APPLE",
        "email": "appleseed@apple.com"
    }
]

# 🏠 HOME ROUTE: Serves up the HTML User Interface
@app.route('/')
def home():
    return render_template('index.html')


# 📂 API ENDPOINT: Read all records OR Create a brand new contact card
@app.route('/api/contacts', methods=['GET', 'POST'])
def handle_contacts():
    global contacts_db
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Construct entry schema payload
        new_contact = {
            "id": len(contacts_db) + 1 if contacts_db else 1,
            "name": data.get("name", "Unknown Node Name"),
            "phone": data.get("phone", "mobile unlisted"),
            "email": data.get("email", "unlisted")
        }
        
        contacts_db.append(new_contact)
        return jsonify(new_contact), 201

    # Default GET execution: Return absolute indexed snapshot array
    return jsonify(contacts_db)


# ⚙️ API ENDPOINT: Update an existing contact card OR Delete it entirely
@app.route('/api/contacts/<int:contact_id>', methods=['PUT', 'DELETE'])
def manage_single_contact(contact_id):
    global contacts_db
    
    # Locate target item in the simulated storage table loop array
    target_contact = next((item for item in contacts_db if item["id"] == contact_id), None)
    
    if not target_contact:
        return jsonify({"error": f"Contact reference ID #{contact_id} not discovered."}), 404

    if request.method == 'PUT':
        update_data = request.get_json()
        
        # Hot-patch modification layers safely 
        target_contact["name"] = update_data.get("name", target_contact["name"])
        target_contact["phone"] = update_data.get("phone", target_contact["phone"])
        target_contact["email"] = update_data.get("email", target_contact["email"])
        
        return jsonify(target_contact), 200

    if request.method == 'DELETE':
        # Re-build directory slice leaving out chosen active node reference
        contacts_db = [item for item in contacts_db if item["id"] != contact_id]
        return jsonify({"message": f"Successfully deleted target identity token index #{contact_id}."}), 200


if __name__ == '__main__':
    # Initialize high-octane local deployment pipeline engine context
    app.run(debug=True, port=5000)