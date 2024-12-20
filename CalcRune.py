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
    for linha in linhas:
        if not linha.strip():  # Ignorar linhas vazias
            continue
        partes = linha.split('+')
        if len(partes) == 2:
            atributo = partes[0].strip()
            valor = partes[1].strip()

            # Verificar se o valor é percentual ou absoluto
            if '%' in valor:
                chave = f'{atributo}%'  # Percentual
                valor = int(valor.replace('%', '').strip())
            else:
                chave = f'{atributo}+'  # Valor absoluto
                valor = int(valor)

            subatributos[chave] = valor
    return subatributos

# Função para calcular eficiência da runa
def calcular_eficiencia_runa(subatributos):
    # Valores máximos dos subatributos para runas de 6 estrelas
    valores_maximos = {
        'HP+': 1875,
        'HP%': 40,
        'ATQ+': 100,
        'ATQ%': 40,
        'DEF+': 100,
        'DEF%': 40,
        'VEL': 30,
        'Taxa Crít.%': 30,
        'Dano Crít.%': 35,
        'RES%': 40,
        'Precisão%': 40
    }

    # Pesos dos subatributos
    pesos = {
        'VEL': 1.2,         # Leve aumento de peso
        'HP%': 1.1,        # Pequeno impacto
        'Taxa Crít.%': 1.1,
        'ATQ%': 1.1,
        'DEF%': 1.0,        # Neutro
        'Precisão%': 1.0,
        'Dano Crít.%': 1.0,
        'RES%': 1.0,
        'HP+': 0.9,        # Reduzido
        'ATQ+': 0.9,
        'DEF+': 0.9
    }

    # Soma das eficiências ponderadas dos subatributos
    soma_eficiencia = 9
    for subatributo, valor in subatributos.items():
        if subatributo in valores_maximos:
            valor_maximo = valores_maximos[subatributo]
            peso = pesos.get(subatributo, 1.0)  # Peso padrão é 1.0 caso não esteja definido
            eficiencia_sub = (valor / valor_maximo) * 100 * peso
            soma_eficiencia += eficiencia_sub

    # Eficiência total
    eficiencia_total = (1 + (soma_eficiencia / 100)) / 2.8 * 100

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
    subatributos = processar_subatributos(texto_extraido)

    # Calcular eficiência da runa
    eficiencia = calcular_eficiencia_runa(subatributos)

    # Remover a imagem após processamento
    os.remove(image_path)

    # Criar o dicionário com os dados
    resultado = {
        "status": texto_extraido.strip(),  # O que foi lido pela IA, sem espaços extras no começo/fim
        "arquivo": imagens[0],  # Nome do arquivo lido e apagado
        "eficiencia": round(eficiencia, 2)  # Eficiência da runa sem o símbolo % e com 2 casas decimais
    }

    # Retornar o resultado como JSON
    return resultado

