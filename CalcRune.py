import os
import json
from PIL import Image
import pytesseract

# Função para extrair texto da imagem
def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)  # Removido lang='por'
        return text
    except Exception as e:
        return f"Erro ao processar a imagem: {e}"

# Função para processar o texto extraído e criar o dicionário de subatributos
def processar_subatributos(texto_extraido):
    subatributos = {}
    linhas = texto_extraido.split('\n')

    # Dicionário de correções para erros comuns de OCR
    correcoes_ocr = {
        "Precisdo": "Precisao",
        "SPD": "VEL",  # Corrigindo "SPD" para "VEL"
        # Adicione mais correções, se necessário
    }

    for linha in linhas:
        if not linha.strip():  # Ignorar linhas vazias
            continue
        partes = linha.split('+')
        if len(partes) == 2:
            atributo = partes[0].strip()
            valor = partes[1].strip()

            # Corrigir erros de OCR no atributo
            atributo_corrigido = correcoes_ocr.get(atributo, atributo)

            # Verificar se o valor é percentual ou absoluto
            if '%' in valor:
                chave = f'{atributo_corrigido}%'  # Percentual
                valor = int(valor.replace('%', '').strip())
            else:
                chave = atributo_corrigido  # Sem o '+', pois é um valor absoluto
                valor = int(valor)

            # Exibir valores para depuração
            print(f"Atributo corrigido: {atributo_corrigido}, Valor: {valor}, Chave: {chave}")

            # Adicionar ao dicionário de subatributos
            subatributos[chave] = valor
    return subatributos

# Função para calcular eficiência da runa
def calcular_eficiencia_runa(subatributos):
    # Valores máximos dos subatributos para runas de 6 estrelas no nível +0
    valores_maximos = {
        'HP+': 375,
        'HP%': 8,
        'ATQ+': 20,
        'ATQ%': 8,
        'DEF+': 20,
        'DEF%': 8,
        'VEL': 6,
        'Taxa Crit.%': 6,
        'Dano Crit.%': 7,
        'RES%': 8,
        'Precisao%': 8
    }

    # Pesos dos subatributos
    pesos = {
        'VEL': 1.3,
        'Taxa Crit.%': 1.2,
        'Dano Crit.%': 1.0,
        'HP%': 1.2,
        'ATQ%': 1.0,
        'DEF%': 1.0,
        'Precisao%': 0.7,
        'RES%': 0.8,
        'HP+': 0.5,
        'ATQ+': 0.5,
        'DEF+': 0.5
    }

    # Soma das eficiências ponderadas dos subatributos
    soma_eficiencia = 0
    for subatributo, valor in subatributos.items():
        if subatributo in valores_maximos:
            valor_maximo = valores_maximos[subatributo]
            peso = pesos.get(subatributo, 1.0)  # Peso padrão é 1.0 caso não esteja definido
            # Calcular a eficiência ponderada, ajustando o valor com o peso e normalizando
            eficiencia_sub = (valor * peso) / valor_maximo * 100
            soma_eficiencia += eficiencia_sub

    # Número de subatributos presentes na runa
    num_subatributos = len(subatributos)

    # Normalizar a eficiência total para não ultrapassar 100%
    eficiencia_total = soma_eficiencia / (num_subatributos * 100) * 100

    # Garantir que a eficiência total não ultrapasse 100%
    eficiencia_total = min(eficiencia_total, 100)

    return eficiencia_total

# Função principal que integra os passos e retorna o resultado formatado como JSON
def calcular_eficiencia_da_runa():
    # Caminho da imagem
    image_path = './cache'

    # Verificar se há uma imagem na pasta ./cache
    imagens = [f for f in os.listdir(image_path) if f.endswith(('png', 'jpg', 'jpeg'))]
    if len(imagens) != 1:
        raise FileNotFoundError("Deve haver exatamente uma imagem no diretório ./cache.")

    image_path = os.path.join(image_path, imagens[0])

    # Etapas do processo
    texto_extraido = extract_text_from_image(image_path)
    
    # Imprimir o texto extraído para diagnóstico
    print("Texto extraído da imagem:", texto_extraido)

    subatributos = processar_subatributos(texto_extraido)

    # Calcular eficiência da runa
    eficiencia = calcular_eficiencia_runa(subatributos)

    os.remove(image_path)

    # Criar o dicionário com os dados
    resultado = {
        "status": texto_extraido.strip(),  # O que foi lido pela IA, sem espaços extras no começo/fim
        "arquivo": imagens[0],  # Nome do arquivo lido e apagado
        "eficiencia": round(eficiencia, 2)  # Eficiência da runa sem o símbolo % e com 2 casas decimais
    }

    # Retornar o resultado como JSON
    return resultado
