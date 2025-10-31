import easyocr

# --- IMPORTANTE ---
# O EasyOCR carrega os modelos de linguagem na memória na primeira vez.
# Para evitar que aconteça a cada requisição (o que seria muito lento),
# inicializamos o 'reader' uma única vez, fora da função da API.
print("Carregando o modelo EasyOCR na memória...")
reader = easyocr.Reader(['pt', 'en'])
print("Modelo carregado com sucesso.")


def analyze_image_easyocr(image_bytes, target_word):
    """
    Analisa imagem usando EasyOCR
    Args:
        image_bytes: bytes da imagem (pode ser JPEG, PNG, etc)
        target_word: palavra a ser procurada no texto extraído
    Returns:
        dict com 'result' (bool) e 'text' (string extraída)
    """
    try:
        # EasyOCR aceita bytes direto
        result_ocr = reader.readtext(image_bytes)
        
        extracted_text = " ".join([text for (bbox, text, prob) in result_ocr])

        if target_word.lower() in extracted_text.lower():
            return { "result" : True, "text" : extracted_text }
        else :
            return { "result" : False, "text" : extracted_text }

    except Exception as e:
        print(f"[ERRO OCR] {str(e)}")
        return { "result" : False, "text" : f"ERRO: {str(e)}" }
