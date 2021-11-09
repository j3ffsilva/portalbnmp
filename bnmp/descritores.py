#!/usr/bin/env python

import pandas as pd
from datetime import date, datetime
import io
import requests
import re

class Descritor(object):

    def __init__(self):
        # UFs
        #self._UFs = {'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul', 'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina', 'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'}
        self._UFs = {'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul', 'PA': 'Pará', 'PB': 'Paraíba', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina', 'SE': 'Sergipe', 'TO': 'Tocantins'}
        self._df = None

    """
    MÉTODOS PÚBLICOS
    """
    def menores_de_idade(self):
        hoje = self._obter_dt_hoje()
        dt_18_anos_atrás = self._obter_dt_18_anos_atrás(hoje)
        return self._df.loc[self._df.dt_nascimento > dt_18_anos_atrás]

    def maiores_penas(self, limiar=10):
        df = self._df.loc[self._df.pena_imposta > limiar]
        return df.sort_values(by=['pena_imposta'], ascending=False)

    def obter_por_UF(self, uf):
        return self._df.loc[self._df.UF == uf]

    def df(self):
        return self._df

    """
    MÉTODOS PRIVADOS
    """
    def _formatar_data(self, data):
        data = str(data)
        data = data.replace(";", "")
        partes = data.split("/")
        if (len(partes) == 3):
            try:
                ano, mes, dia = int(partes[2]), int(partes[1]), int(partes[0])
                if (ano < 1930):
                    raise ValueException("Data Inválida")
                nova_data = datetime().strftime("%Y-%m-%d")
                return nova_data
            except:
                pass
        return None

    def _obter_dt_hoje(self):
        return date.today().strftime("%Y-%m-%d")

    def _obter_dt_18_anos_atrás(self, hoje):
        este_ano, este_mes, este_dia = hoje.split("-")
        aquele_ano = str(int(este_ano) - 18)
        return aquele_ano + "-" + este_mes + "-" + este_dia

class DescritorLocal(Descritor):

    def __init__(self, base_caminho_dados=None):
        super().__init__()

        base_caminho_dados = "dados/tsv/" if not base_caminho_dados else base_caminho_dados

        frames = []
        for uf in self._UFs:
            arq = base_caminho_dados + uf + '.tsv'
            frames.append(pd.read_csv(arq, sep='\t'))

        df = pd.concat(frames)

        # Transforma para o tipo de dados data
        df.dt_nascimento = df.dt_nascimento.apply(self._formatar_data)
        df.dt_nascimento = pd.to_datetime(df.dt_nascimento)
        self._df = df

class DescritorRemoto(Descritor):

    def __init__(self, url_base_dados=None):
        super().__init__()
        # URL dos dados
        self._url_base_dados = "https://raw.githubusercontent.com/j3ffsilva/portalbnmp/master/dados/tsv/" if not url_base_dados else url_base_dados

        frames = []
        for uf in self._UFs:
            url = self._url_base_dados + uf + '.tsv'
            conteúdo = requests.get(url).content
            conteúdo_utf8 = io.StringIO(conteúdo.decode('utf-8'))
            frames.append(pd.read_csv(conteúdo_utf8, sep='\t'))

        df = pd.concat(frames)
        # Transforma para o tipo de dados data
        df.dt_nascimento = df.dt_nascimento.apply(self._formatar_data)
        df.dt_nascimento = pd.to_datetime(df.dt_nascimento)
        self._df = df
