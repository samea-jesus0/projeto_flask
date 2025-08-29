from flask import Flask, request, jsonify 
import socket

app = Flask(__name__)

users = [
    {"id": 1, "nome": "samea", "email": "sameasilva@gmail.com"}
]

id_usuarios = 3

@app.route('/users', methods=['GET'])
def mostrar_usuarios():
    if not users:
        return users, 200
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    
    if user:
        return jsonify(user), 200
    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route('/users', methods=['POST'])
def criar_usuario():
    global id_usuarios
    new_user_data = request.json
    
    if not new_user_data or 'nome' not in new_user_data or 'email' not in new_user_data:
        return jsonify({"message": "Dados incompletos"}), 400

    new_user = {
        "id": id_usuarios,
        "nome": new_user_data["nome"], 
        "email": new_user_data["email"] 
    }
    
    users.append(new_user)
    id_usuarios += 1
    
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def att_usuario(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
        
    update_data = request.json
    
    user["nome"] = update_data.get("nome", user["nome"])
    user["email"] = update_data.get("email", user["email"])
     
    return jsonify(user), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def apagar_usuario(user_id):
    global users
    user_to_delete = next((user for user in users if user["id"] == user_id), None)

    if not user_to_delete:
        return jsonify({"message": "Usuário não encontrado"}), 404
        
    users = [user for user in users if user["id"] != user_id]
    
    return jsonify({"message": "Usuário excluído com sucesso"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)