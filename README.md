# LembreX API Image

API REST para validação de texto em imagens através de OCR (Optical Character Recognition).

## Descrição

API desenvolvida em Python/Flask que utiliza EasyOCR para extrair e validar texto em imagens. Processa duas imagens codificadas em Base64 e verifica se ambas contêm o texto alvo especificado.

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

### Desenvolvimento Local

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

### Produção

A API está hospedada em: **http://51.21.127.221/**

## Documentação da API

### GET `/`

Rota de verificação de status.

**Resposta:**
- HTML com link para documentação

---

### POST `/api`

Processa duas imagens e verifica se ambas contêm o texto especificado.

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "text": "palavra-alvo",
  "images": [
    "base64_encoded_image_1",
    "base64_encoded_image_2"
  ]
}
```

**Parâmetros:**
- `text` (string, obrigatório): Texto a ser localizado nas imagens
- `images` (array, obrigatório): Array com exatamente 2 imagens codificadas em Base64

**Respostas:**

**200 OK** - Texto encontrado em ambas as imagens
```json
{
  "success": true,
  "message": "A palavra {text} foi encontrada em ambas as imagens!",
  "data": [
    {
      "first_image": true,
      "extracted_text": "texto extraído da primeira imagem"
    },
    {
      "second_image": true,
      "extracted_text": "texto extraído da segunda imagem"
    }
  ]
}
```

**404 Not Found** - Texto não encontrado em uma ou ambas as imagens
```json
{
  "success": false,
  "message": "Problema ao encontrar a palavra: {text} em ambas as imagens!",
  "data": [
    {
      "first_image": false,
      "extracted_text": "texto extraído da primeira imagem"
    },
    {
      "second_image": false,
      "extracted_text": "texto extraído da segunda imagem"
    }
  ]
}
```

**400 Bad Request** - Dados inválidos ou incompletos
```json
{
  "success": false,
  "message": "Dados inválidos"
}
```

OU

```json
{
  "success": false,
  "message": "Duas imagens são necessárias"
}
```

## Exemplo de Uso

```bash
curl -X POST http://localhost:5000/api \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Paracetamol",
    "images": [
      "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
      "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    ]
  }'
```

## Tecnologias

- Python 3.x
- Flask 3.0.0
- EasyOCR 1.7.0
- Gunicorn 22.0.0

## Parte do Sistema LembreX

Esta API integra o sistema [LembreX](https://github.com/joaovic-tech/lembrex) para validação de medicamentos através de reconhecimento óptico de caracteres.
