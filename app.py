from flask import Flask, request, jsonify, send_from_directory
from api.modelo import clasificar_cuenta

app = Flask(__name__, static_url_path='')

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/clasificar', methods=['POST'])
def clasificar():
    data = request.json
    nombre_cuenta = data.get('nombre_cuenta')
    if not nombre_cuenta:
        return jsonify({"error": "Falta el nombre de la cuenta"}), 400
    
    resultado = clasificar_cuenta(nombre_cuenta)
    return jsonify(resultado)

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# No uses esto en Vercel
# if __name__ == '__main__':
#     app.run(debug=True)