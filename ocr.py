import base64
import easyocr
import re
import logging

logger = logging.getLogger(__name__)

# --- IMPORTANTE ---
# O EasyOCR carrega os modelos de linguagem na memória na primeira vez.
# Para evitar que aconteça a cada requisição (o que seria muito lento),
# inicializamos o 'reader' uma única vez, fora da função da API.
print("Carregando o modelo EasyOCR na memória...")
reader = easyocr.Reader(['pt', 'en'])
print("Modelo carregado com sucesso.")


def clean_base64(base64_string):
    """Remove data URL prefix if present and clean base64 string"""
    # Remove data URL prefix (data:image/...;base64,)
    if base64_string.startswith('data:'):
        base64_string = re.sub(r'^data:image/[^;]+;base64,', '', base64_string)
    
    # Remove any whitespace
    base64_string = re.sub(r'\s+', '', base64_string)
    
    return base64_string

def analyze_image_easyocr(image_base64, target_word):
    try:
        logger.info(f"Analisando imagem, procurando por: '{target_word}'")
        
        # Limpar string base64
        clean_b64 = clean_base64(image_base64)
        logger.info(f"Base64 limpo, tamanho: {len(clean_b64)} caracteres")
        
        # Decodificar base64
        try:
            bytes_image = base64.b64decode(clean_b64)
            logger.info(f"Imagem decodificada, tamanho: {len(bytes_image)} bytes")
        except Exception as decode_error:
            logger.error(f"Erro ao decodificar base64: {decode_error}")
            return {"err": f"Erro na decodificação base64: {str(decode_error)}"}
        
        # Processar OCR
        logger.info("Executando OCR na imagem...")
        result_ocr = reader.readtext(bytes_image)
        logger.info(f"OCR concluído, encontrados {len(result_ocr)} elementos de texto")
        
        # Extrair texto
        extracted_text = " ".join([text for (bbox, text, prob) in result_ocr])
        logger.info(f"Texto extraído: '{extracted_text}'")
        
        # Verificar se a palavra alvo foi encontrada
        found = target_word.lower() in extracted_text.lower()
        logger.info(f"Palavra '{target_word}' encontrada: {found}")

        return { 
            "result": found, 
            "text": extracted_text 
        }

    except Exception as e:
        logger.error(f"Erro no processamento OCR: {str(e)}")
        return {"err": str(e)}
