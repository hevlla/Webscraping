import json

dicionario = dict(nome = ["Manoel", "Rubem", "Marcelo", "Henrique"], cidade = ["Berlim", "Toronto", "Campina Grande", "Estados Unidos"], problema = ["bullying", "estupro", "fanatismo", "drogas", "desarmamento"])
dict_salvar = json.dumps(dicionario, indent = 4, sort_keys = True)  #indent= deixar organizado e visivel e sort_keys= ordem alfabetica

#Criando um arquivo json
arquivo_json = open("segunda_analise.json", "w")   #w= cria um arquivo
arquivo_json.write(dict_salvar)            #Escreve no arquivo
arquivo_json.close()

#Abrindo o arquivo json
arquivo_json = open("segunda_analise.json", 'r')   #r= ler o arquivo
Analise_cancer = json.load(arquivo_json)   #load= carrega o arquivo

