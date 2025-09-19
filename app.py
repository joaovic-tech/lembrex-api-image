from flask import Flask, request, jsonify

from ocr import analyze_image_easyocr as ocr

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


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
