# LembreX API Image

> API Python para processamento OCR de medicamentos - Parte do sistema [LembreX](https://github.com/joaovic-tech/lembrex)

## Sobre

Este repositório contém a API Python responsável pela validação de medicamentos através de OCR (Optical Character Recognition). O sistema analisa imagens enviadas pelo app Android e verifica se o nome do medicamento na caixa corresponde ao medicamento que deveria ser tomado.

Futuramente pode ser usado para qualquer tipo de aplicacão que precisa verificar se duas ou mais imagens tem um texto identificador

## Para que serve esse repositório?

Serve para ajudar a realizar e identificar se um determinado texto possui nas imagens enviadas

## Colo funciona?

A api recebe um objeto json contendo duas imagens e texto alvo para verificacão, usando a lib ocr do python ele extrai texto das imagens e verifica se dentro desse texto possui o texto alvo.