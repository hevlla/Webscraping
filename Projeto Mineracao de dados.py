"""
Projeto Web Scraping. Alunos: Hevlla Oliveira Souza e Rubem Ribeiro Barros. Professores: Marcelo Siqueira e Henrique Cunha.
Data de Finalizacao: 20 de setembro de 2017.
"""

import time
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import json
import requests
from bs4 import BeautifulSoup

def extrair_html(url):
    '''
    Extrai o html dos sites
    '''
    url = url.replace("\n", "")                                         # Troca "\n" por vazio
    url.encode('utf-8')                                                 # Codifica para 'utf-8'
    try:
        requisicao = requests.get(url)
        html_requisicao = requisicao.content                            # Recebe a resposta da requesicao
        status_requisicao = requisicao.status_code                      # Recebe o status do site
        if status_requisicao == requests.codes.ok:                      # Verifica a disponibilidade do site
            html = BeautifulSoup(html_requisicao, "html.parser")        # Recebe o tipo html
        else:
            html = ""
        return html                                                     # Requisita ao site
    except requests.exceptions.RequestException as i:                   # Tratamento de excecao caso a nao tenha internet
        time.sleep(4)
        print("Sem conexao com a internet.\n"
              "Tente novamente mais tarde.")
        sys.exit()

def minerar(html):
    '''
    Minera os paragrafos e as tabelas do html
    '''
    textos = []
    minerar_paragrafo = html.select('body p')                           # Recebe os paragrafos
    minerar_tabela = html.select('body tr')                             # Recebe as tabelas
    tags_html = minerar_paragrafo + minerar_tabela                      # Recebe em una unica lista os paragrafos e as tabelas
    for tag in tags_html:                                               # Percorre a lista com os paragrafos e as tabelas
        textos.append(tag.get_text().lower())                           # Adiciona na lista "textos" o texto retirado do html, em minusculo
    return textos

def analisar(nome_json, txt):
    """
    Analise da frequencia dos elementos nas chaves
    """
    with open('/home/hevilla/PycharmProjects/Projeto Algoritmos/analises/' + nome_json, "r") as caminho_arquivo_json:
        arquivo_json = json.load(caminho_arquivo_json)
        elementos_chave = arquivo_json[entrada_usuario]                 # Abertura da chave do dicionario(json)

    # Analise dos elementos presentes
    for elemento in elementos_chave:                                    # Pesquisar se existe os elementos no arquivo txt
        nomes_elementos.append(elemento)                                # Adicao dos elementos para criacao dos graficos
        frequencia_jsons.append(txt.count(elemento.lower()))
    return nomes_elementos, frequencia_jsons

def criar_grafico(nomes, frequencias, tipo_dado, url):
    '''
    Grafico dos jsons
    '''
    fig, ax = plt.subplots(figsize=(16, 9))                             # Atribuicao em uma tupla: fig= tupla de variaveis e ax= tupla de valores
    qtd_elementos = np.arange(len(nomes))                               # Quantidade de elementos na lista
    ax.bar(qtd_elementos, frequencias, align='center',
           color='blue', alpha=0.6)                                     # (x, y, janela no meio da tela, cor)
    ax.set_xticks(qtd_elementos)
    ax.set_ylim(0, 10)
    ax.set_xticklabels(nomes, weight=550, rotation= 25)                 # weight= Negrito
    ax.set_ylabel('Frequencia', weight=550)
    ax.set_title('Frequencia de ' + tipo_dado + 's\nSite: ' + url,
                 weight=750, size='medium', style='italic')
    plt.show()

# Recebendo e validando a chave presente no arquivo json
while True:
  estetica= "-" * 49
  espaco = " " * 12
  analise_json = ["cidade", "nome", "problema"]
  entrada_usuario = input(estetica + " Informe o que deseja procurar: "+ estetica + "\n\n"
                      + espaco*3 + " ()Nome" + espaco + "()Cidade"
                      + espaco + "()Problema\n").lower()
  if entrada_usuario not in analise_json:                               #Verificar se a chave existe
      print("\n" + estetica + espaco + " ERROR " +espaco + estetica + '\n\n\n')
  else:
      break

# Realizando a Web Scraping
urls = open('urls.txt', 'r')
for url in urls:                                                        # Percorrer o arquivo txt com as urls
    html = extrair_html(url)
    if html == "":
        print("ERRO")
        continue
    textos = minerar(html)

    # Adicionando os dados em um arquivo .txt (body)
    arquivo_txt = open("texto.txt", "w")
    for texto in textos:
        arquivo_txt.write(texto)                                        # Adicao do texto retirado, em um arquivo .txt
    arquivo_txt.close()

    #Lendo o arquivo .txt
    arquivo_txt = open("texto.txt", "r")                                # Leitura do txt
    modo_leitura_txt = arquivo_txt.read()

    #Diretorio
    diretorio_jsons = os.listdir('analises')
    frequencia_jsons = []                                               # Limpeza das listas
    nomes_elementos = []
    # Lendo o arquivo txt e o json
    for nome_json in diretorio_jsons:
        time.sleep(1)
        nomes_elementos_, frequencia_jsons_ = analisar(nome_json, modo_leitura_txt)
    criar_grafico(nomes_elementos, frequencia_jsons, entrada_usuario, url)

