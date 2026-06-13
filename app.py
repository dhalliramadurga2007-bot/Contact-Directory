from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DB_FILE = "contacts.json"

def load_contacts():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_contacts(contacts):
    with open(DB_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

# API: Get all contacts
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    return jsonify(load_contacts())

# API: Add a new contact
@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.json
    if not data or not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
        
    contacts = load_contacts()
    # Simple ID generation strategy
    new_id = max([c.get('id', 0) for c in contacts]) + 1 if contacts else 1
    
    new_contact = {
        "id": new_id,
        "name": data.get('name'),
        "phone": data.get('phone', 'N/A'),
        "email": data.get('email', 'N/A')
    }
    contacts.append(new_contact)
    save_contacts(contacts)
    return jsonify({"message": "Contact added!", "contact": new_contact}), 201

# API: Save modifications (Edit)
@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.json
    contacts = load_contacts()
    
    for c in contacts:
        if c.get('id') == contact_id:
            c['name'] = data.get('name', c['name'])
            c['phone'] = data.get('phone', c['phone'])
            c['email'] = data.get('email', c['email'])
            save_contacts(contacts)
            return jsonify({"message": "Contact updated successfully!", "contact": c})
            
    return jsonify({"error": "Contact not found"}), 404

# API: Delete a contact
@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    contacts = load_contacts()
    updated_contacts = [c for c in contacts if c.get('id') != contact_id]
    
    if len(contacts) == len(updated_contacts):
        return jsonify({"error": "Contact not found"}), 404
        
    save_contacts(updated_contacts)
    return jsonify({"message": "Contact deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)