from flask import Flask, request, jsonify

from ocr import analyze_image_easyocr as ocr

app = Flask(__name__)


@app.route('/')
def hello():
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LEMBREX API IMAGE</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f2f5;
                color: #333;
                text-align: center;
            }
            a { color: #007BFF; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div>
            <h1>Conectado a LEMBREX API IMAGE</h1>
            <p><a href="https://github.com/joaovic-tech/lembrex-api-image/blob/main/README.md" target="_blank" rel="noopener noreferrer">Acessar Documentação</a></p>
        </div>
    </body>
    </html>
    '''

# Pegar o body em formato json
@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    if not data or "text" not in data or "images" not in data:
        return jsonify({"success": False, "message": "Dados inválidos"}), 400
    if len(data["images"]) < 2:
        return jsonify({"success": False, "message": "Duas imagens são necessárias"}), 400

    text = request.json.get('text')
    images = request.json.get('images')

    find_text_remedy = ocr(images[0], text)
    find_text_remedy_user = ocr(images[1], text)

    if find_text_remedy.get("result") and find_text_remedy_user.get("result"):
        return jsonify({
            "success": True,
            "message": f"A palavra {text} foi encontrada em ambas as imagens!",
            "data": [
                {"first_image": find_text_remedy.get("result"), "extracted_text": find_text_remedy.get("text")},
                {"second_image": find_text_remedy_user.get("result"),
                 "extracted_text": find_text_remedy_user.get("text")}
            ],
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": f"Problema ao encontrar a palavra: {text} em ambas as imagens!",
            "data": [
                {"first_image": find_text_remedy.get("result"), "extracted_text": find_text_remedy.get("text")},
                {"second_image": find_text_remedy_user.get("result"),
                 "extracted_text": find_text_remedy_user.get("text")}
            ],
        }), 404


if __name__ == '__main__':
    app.run()