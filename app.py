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

# Receber imagens via multipart/form-data
@app.route('/api', methods=['POST'])
def api():
    # Verificar se os campos necessários estão presentes
    if 'text' not in request.form:
        return jsonify({"success": False, "message": "Campo 'text' é obrigatório"}), 400
    
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"success": False, "message": "Duas imagens são necessárias (image1 e image2)"}), 400

    text = request.form.get('text')
    image1_bytes = request.files['image1'].read()
    image2_bytes = request.files['image2'].read()

    find_text_remedy = ocr(image1_bytes, text)
    find_text_remedy_user = ocr(image2_bytes, text)

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