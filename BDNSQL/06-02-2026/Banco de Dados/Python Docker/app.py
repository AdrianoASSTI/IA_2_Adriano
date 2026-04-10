from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>🚀 App rodando dentro do Docker com sucesso!</h1>'

if __name__ == '__main__':
    # host 0.0.0.0 permite que o container seja acessado de fora
    app.run(debug=True, host='0.0.0.0', port=5000)