import os
import glob
import datetime
from datetime import date, timedelta
import requests
from imap_tools import MailBox, AND
import datetime
import pandas
import pathlib
from time import sleep

# enviar mensagens utilizando o bot para um chat específico
def send_message(token, chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": message}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e)

# token único utilizado para manipular o bot (não deve ser compartilhado), token é criado pelo BotFather
token = ''

# id do chat que será enviado as mensagens
chat_id = 1

#Variáveis para armazenar hora das validações
agora = datetime.datetime.now()
meiodia = datetime.datetime(agora.year,agora.month,agora.day,12,00)
valida_audios = datetime.datetime(agora.year,agora.month,agora.day,13,00)

#Montar nome do arquivo METADATA que será validado no dia
dia_semana = date.today().weekday()

if dia_semana == 0:
    ontem = datetime.datetime.now() - timedelta(days=3)
else:
    ontem = datetime.datetime.now() - timedelta(days=1)

metadata = ontem.strftime('%d%m%Y') + "_METADATA.xlsx"

#Variáveis contadoras para validações
value1 = 0
value2 = 0
value3 = 0
comdata = 0

try:
    #Looping
    while value1 <= 0:
        sleep(30)
        #Abre a planilha e conta a quantidade de linhas em ATC/ CSF
        data = pandas.read_excel("L:/COBRANCA_PRE/" + metadata)
        #Armazena quantidade de linhas de ATC/ CSF
        condicao = data['produto']
        atc = 0
        crf = 0
        #Faz a contagem das linhas
        for i in condicao:
            if i == "CRF":
                crf = crf + 1
            else:
                atc = atc + 1

        total = crf + atc    

        #Monta o texto e envia para o Telegram
        msg = f"""Metadados {ontem.strftime('%d/%m/%Y')}\nATC: {atc}\nCSF: {crf}\nTotal: {total} registros"""
        send_message(token, chat_id, msg)
        value1 = 1

    #Looping
    while value2 <= 0:
        sleep(30)
        #Valida hora atual para validações
        agora = datetime.datetime.now()
        #Especifica o diretório/ nome para busca do arquivo
        os.chdir('L:/COBRANCA_PRE/Selecionados/')
        files = glob.glob(metadata)

        try:
            #Caso encontre o arquivo, irá terminar o looping e irá enviar a mensagem no Telegram
            if files != []:
                #Abre a planilha e conta a quantidade de áudios selecionados        
                data = pandas.read_excel("L:/COBRANCA_PRE/Selecionados/" + metadata)
                qtd_linhas = data['Selecionados'].sum()
                #Monta o texto e envia para o Telegram
                msg = "Arquivo consta no SFTP com " + str(int(qtd_linhas)) + " áudios selecionados"
                send_message(token, chat_id, msg)
                value2 = 1
        except Exception as e:
            msg = "Erro: " + str(e)
            send_message(token, chat_id, msg)	
            pass

        #Caso não encontre o arquivo, irá nos avisar no Telegram para acionarmos a COMDATA
        if agora > meiodia and comdata == 0:
            msg = "Arquivo com os áudios selecionados não consta no SFTP, acionar COMDATA!"
            send_message(token, chat_id, msg)
            comdata = 1

    #Looping
    while value3 <= 0:
        sleep(30)
        #Valida hora atual para validações
        agora = datetime.datetime.now()
        if agora > valida_audios:    
            audios = 0 
            #Realiza a contagem dos áudios no caminho
            for path in pathlib.Path("L:/COBRANCA_PRE/Selecionados/Importados").iterdir():
                if path.is_file():
                    audios += 1
            #Monta o texto e envia para o Telegram
            msg = str(audios) + " áudios enviados ao SFTP!"
            send_message(token, chat_id, msg)
            value3 = 1
        
except Exception as e:
        msg = "Erro: " + str(e)
        send_message(token, chat_id, msg)