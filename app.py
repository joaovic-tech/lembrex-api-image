from flask import Flask, request, jsonify
import logging
import sys

from ocr import analyze_image_easyocr as ocr

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


# Pegar o body em formato json
@app.route('/api', methods=['POST'])
def api():
    try:
        logger.info("=== Nova requisição recebida ===")
        logger.info(f"Content-Type: {request.content_type}")
        logger.info(f"Content-Length: {request.content_length}")
        
        data = request.get_json()
        if not data:
            logger.error("Nenhum JSON recebido")
            return jsonify({"success": False, "message": "Nenhum JSON encontrado no body"}), 400
            
        if "text" not in data:
            logger.error("Campo 'text' não encontrado no JSON")
            return jsonify({"success": False, "message": "Campo 'text' é obrigatório"}), 400
            
        if "images" not in data:
            logger.error("Campo 'images' não encontrado no JSON")
            return jsonify({"success": False, "message": "Campo 'images' é obrigatório"}), 400
            
        if not isinstance(data["images"], list) or len(data["images"]) < 2:
            logger.error(f"Campo 'images' deve ter pelo menos 2 itens. Recebido: {len(data.get('images', []))}")
            return jsonify({"success": False, "message": "Duas imagens são necessárias"}), 400

        text = data.get('text')
        images = data.get('images')
        
        logger.info(f"Texto a procurar: '{text}'")
        logger.info(f"Número de imagens recebidas: {len(images)}")
        for i, img_b64 in enumerate(images):
            img_size = len(img_b64) if img_b64 else 0
            logger.info(f"Imagem {i+1}: {img_size} caracteres base64")

        logger.info("Iniciando processamento OCR...")
        
        # Processar primeira imagem
        logger.info("Processando primeira imagem...")
        find_text_remedy = ocr(images[0], text)
        logger.info(f"Resultado primeira imagem: {find_text_remedy.get('result')}")
        
        # Processar segunda imagem
        logger.info("Processando segunda imagem...")
        find_text_remedy_user = ocr(images[1], text)
        logger.info(f"Resultado segunda imagem: {find_text_remedy_user.get('result')}")
        
        # Verificar se houve erros no OCR
        if "err" in find_text_remedy or "err" in find_text_remedy_user:
            error_msg = find_text_remedy.get("err") or find_text_remedy_user.get("err")
            logger.error(f"Erro no processamento OCR: {error_msg}")
            return jsonify({
                "success": False,
                "message": f"Erro no processamento de imagem: {error_msg}"
            }), 500

        if find_text_remedy.get("result") and find_text_remedy_user.get("result"):
            logger.info(f"Sucesso! Palavra '{text}' encontrada em ambas as imagens")
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
            logger.warning(f"Palavra '{text}' não encontrada em ambas as imagens")
            return jsonify({
                "success": False,
                "message": f"Problema ao encontrar a palavra: {text} em ambas as imagens!",
                "data": [
                    {"first_image": find_text_remedy.get("result"), "extracted_text": find_text_remedy.get("text")},
                    {"second_image": find_text_remedy_user.get("result"),
                     "extracted_text": find_text_remedy_user.get("text")}
                ],
            }), 404
    
    except Exception as e:
        logger.error(f"Erro inesperado na API: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Erro interno do servidor: {str(e)}"
        }), 500


if __name__ == '__main__':
    logger.info("Iniciando servidor Flask...")
    logger.info("API disponível em:")
    logger.info("  - Localhost: http://127.0.0.1:5000")
    logger.info("  - Emulador Android: http://10.0.2.2:5000")
    logger.info("  - Rede local: http://0.0.0.0:5000")
    
    # Configurar para aceitar conexões externas (emulador)
    app.run(
        host='0.0.0.0',  # Aceita conexões de qualquer IP
        port=5000,
        debug=True  # Ativar debug em desenvolvimento
    )
