import base64
import easyocr

# --- IMPORTANTE ---
# O EasyOCR carrega os modelos de linguagem na memória na primeira vez.
# Para evitar que aconteça a cada requisição (o que seria muito lento),
# inicializamos o 'reader' uma única vez, fora da função da API.
print("Carregando o modelo EasyOCR na memória...")
reader = easyocr.Reader(['pt', 'en'])
print("Modelo carregado com sucesso.")


def analyze_image_easyocr(image_base64, target_word):
    try:
        bytes_image = base64.b64decode(image_base64)
        result_ocr = reader.readtext(bytes_image)
        
        print(f"\n[OCR] Procurando por: '{target_word}'")
        print(f"[OCR] Resultados detectados: {len(result_ocr)} textos")
        
        extracted_text = " ".join([text for (bbox, text, prob) in result_ocr])
        
        print(f"[OCR] Texto extraído: '{extracted_text}'")
        print(f"[OCR] Palavra encontrada: {target_word.lower() in extracted_text.lower()}")

        if target_word.lower() in extracted_text.lower():
            return { "result" : True, "text" : extracted_text }
        else :
            return { "result" : False, "text" : extracted_text }

    except Exception as e:
        print(f"[OCR] Erro: {str(e)}")
        return {"err": str(e)}
