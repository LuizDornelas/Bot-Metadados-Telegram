import os
import pandas as pd
import telepot
import datetime
from datetime import date, timedelta

# Inicializa o bot do Telegram
bot = telepot.Bot("")
chat_id = -1

#Montar nome do arquivo METADATA que será validado no dia
dia_semana = date.today().weekday()

if dia_semana == 0:
    ontem = datetime.datetime.now() - timedelta(days=2)
else:
    ontem = datetime.datetime.now() - timedelta(days=1)

data = "C:/santander/sftp/" + ontem.strftime('%d-%m') + "/"
metadata_txt = data + ontem.strftime('%d%m%Y') + "_metadado.txt"

#Variáveis contadoras para validações

try:
    # Lê o arquivo txt usando a biblioteca pandas
    df = pd.read_csv(metadata_txt, delimiter=",")

    # Conta os dados da coluna 8
    counts = df.iloc[:,7].value_counts()

    # Conta o total de dados na coluna 8
    total = df.iloc[:,7].count()

    # Conta a quantidade de arquivos na pasta especificada
    qtd_arquivos = len(os.listdir(data))

    # Formata a mensagem com a contagem dos dados organizados por quantidade, o total de dados na coluna 8 e a quantidade de arquivos na pasta especificada
    mensagem = "Metadados STD "+ ontem.strftime('%d/%m') + ":\n\n"
    for value, count in counts.iteritems():
        mensagem += "{}: {}\n".format(value, count)
    mensagem += "\nTotal: {}\n".format(total+1)
    mensagem += "\nÁudios enviados: {}".format(qtd_arquivos-1)

    # Envia a mensagem com as informações
    bot.sendMessage(chat_id, mensagem)
    
except Exception as e:
        msg = "Erro: " + str(e)
        bot.sendMessage(chat_id, msg)