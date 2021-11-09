#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import sys
import pandas as pd

class ExtratorBNMP:
    """
    O ExtratorBNMP é uma classe utilitária que facilita a extração das informações contidas no Banco Nacional de Mandados de Prisão
    """
    def __init__(self, elems_pag=10, interv_pag=0.5, raspar_1a_pag = False, driver=None):
        """
        Construtor
        """
        # É possível injetar um driver previamente criado
        self.driver = webdriver.Chrome(self._bnmp_url) if not driver else driver
        self.driver.get("https://portalbnmp.cnj.jus.br/")

        self.num_mandados = {}
        self.mandados = []

        # Número de mandados por página
        self.ELEMS_POR_PAG = elems_pag

        # Intervalo de tempo entre as páginas (dado em segundos)
        self.INTERVALO = interv_pag

        # UFs
        self.UFs = ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins']

        # Raspar somente a primeira página
        self.RASPAR_SOMENTE_1a_PAG = raspar_1a_pag

    def selecionar_UF(self, uf):
        """
        Seleciona a UF baseada na lista dropdown do site
        Args
            uf: UF a ser extraída. Exemplo "Acre"
        """
        dropdown = self.driver.find_element_by_xpath("""//*[@id="ui-fieldset-1-content"]/div/form/div[6]/div/p-dropdown/div/div[2]""")
        # dropdown.click()
        self.driver.execute_script("arguments[0].click();", dropdown)

        # Obtém o input
        cmp_input = self.driver.find_element_by_xpath("""//*[@id="ui-fieldset-1-content"]/div/form/div[6]/div/p-dropdown/div/div[3]/div[1]/input""")

        # Primeiro deleta o texto que estiver no campo
        cmp_input.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)

        sleep(self.INTERVALO)

        # Envia o nome da UF para o campo
        cmp_input.send_keys(uf)

        sleep(self.INTERVALO)

        # Seleciona o estado resultante
        cmp_li = self.driver.find_element_by_xpath("""//*[@id="ui-fieldset-1-content"]/div/form/div[6]/div/p-dropdown/div/div[3]/div[2]/ul/li""")

        # Clica no pesquisar do estado para preencher com o nome
        # cmp_li.click()
        self.driver.execute_script("arguments[0].click();", cmp_li)

        sleep(self.INTERVALO)

        botão_pesq = self.driver.find_element_by_xpath("""//*[@id="ui-fieldset-1-content"]/div/form/div[14]/button[2]""")
        # botão_pesq.click()
        self.driver.execute_script("arguments[0].click();", botão_pesq)

        sleep(self.INTERVALO)

        btn_1a_pag = self.driver.find_element_by_xpath("""/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-datatable/div/p-paginator/div/a[1]""")
        if (self.__btn_esta_habilitado(btn_1a_pag)):
            # btn_1a_pag.click()
            self.driver.execute_script("arguments[0].click();", btn_1a_pag)
            sleep(self.INTERVALO)

    def extrair_tudo(self):
        """
        """
        # Extrai os números dos mandados
        self.extrair_num_mandados()

        # Para cada número de mandado, obtenha os detalhes
        for k in self.num_mandados:
            UF = k
            for num_mandado in self.num_mandados[UF]:
                tipo_peça = self.detalhar(num_mandado)
                mandado = None
                if (tipo_peça == "Mandado de Internação"):
                    mandado = self.extrair_mand_internacao()
                elif (tipo_peça == "Mandado de Prisão"):
                    mandado = self.extrair_mand_prisao()
                else:
                    continue
                #mandado.insert(0, num_peca)
                mandado.insert(0, UF)
                self.mandados.append(mandado)
        self.to_tsv()

    def to_tsv(self, sep='\t'):
        nomes_cols = ["UF", "Tipo Mandado", "Situação", "Número Mandado", "Data de Expedição", "Data de Validade", "Número Processo", "Espécie de Prisão", "Motivo Internação", "Nome Magistrado", "Órgão Expedidor", "Munícipio", "Tipificações Penais", "Nome", "Nacionalidade", "Naturalidade", "Data Nascimento", "Sexo", "Recaptura", "Pena Imposta", "Regime"]
        df = pd.DataFrame(self.mandados, columns=nomes_cols)
        df.to_csv('data/mandados.tsv', sep=sep)

    def extrair_num_mandados(self):
        """
        Extrai as informações dos mandados da capa de todas as UFs
        """
        for uf in self.UFs:
            # Seleciona uma UF
            self.selecionar_UF(uf)

            # Extrai os números de mandado da capa
            self.raspar_mandado_capa(uf)

    def __btn_esta_habilitado(self, btn):
        """
        Verifica se o botão está habilitado
        Args:
            btn
        Retorna
            boolean
        """
        return not "ui-state-disabled" in btn.get_attribute("class")

    def raspar_mandado_capa(self, uf):
        """
        Extrai informações das páginas para a UF selecionada
        Args:
            uf: UF a ser extraída. Exemplo "Acre"
        """
        sleep(self.INTERVALO)
        devo_raspar_pag = True
        lst_mandados = []

        while(devo_raspar_pag):

            for i in range(1,self.ELEMS_POR_PAG+1):
                try:
                    # Obtém o número do mandado
                    xpath_elem = f"/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-datatable/div/div[1]/table/tbody/tr[{i}]/td[1]/span[2]/span"
                    num_mandado = self.driver.find_element_by_xpath(xpath_elem)

                    # Armazena o número do mandado numa lista
                    lst_mandados.append(num_mandado.text)
                except NoSuchElementException:
                    break

            btn_prox = self.driver.find_element_by_xpath("""/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-datatable/div/p-paginator/div/a[3]""")
            if (self.__btn_esta_habilitado(btn_prox) and not self.RASPAR_SOMENTE_1a_PAG):
                # Se o botão de próximo estiver habilitado, então clica n botão
                # btn_prox.click()
                self.driver.execute_script("arguments[0].click();", btn_prox)
                sleep(self.INTERVALO)
            else:
                devo_raspar_pag = False

        self.num_mandados[uf] = lst_mandados

    def detalhar(self, n_peca):
        """
        """

        # Clica no menu pesquisar mandados
        mnu_pesq_mandados_xpath = """/html/body/app-root/div/div/div[1]/div/div[1]/app-menu/ul/li[1]/a/span[1]"""
        mnu_pesq_mandados = self.driver.find_element_by_xpath(mnu_pesq_mandados_xpath)
        # mnu_pesq_mandados.click()
        self.driver.execute_script("arguments[0].click();", mnu_pesq_mandados)

        sleep(self.INTERVALO)

        # Encontra e preenche o numero da peça
        cmp_pesq_xpath = "/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-fieldset/fieldset/div/div/form/div[9]/span/p-inputmask/input"
        cmp_pesquisa = self.driver.find_element_by_xpath(cmp_pesq_xpath)
        cmp_pesquisa.send_keys(n_peca)

        sleep(self.INTERVALO)

        # Encontra e clica no botão de pesquisar
        button_pesq = self.driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-fieldset/fieldset/div/div/form/div[14]/button[2]")
        # button_pesq.click()
        self.driver.execute_script("arguments[0].click();", button_pesq)

        sleep(self.INTERVALO + self.INTERVALO)

        # tipo peca
        tipo_peca = None
        try:
            tipo_peca_xpath = "/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-datatable/div/div[1]/table/tbody/tr/td[6]/span[2]"
            tipo_peca_cmp = self.driver.find_element_by_xpath(tipo_peca_xpath)
            tipo_peca = tipo_peca_cmp.text

            ## Clica no processo para exibir os detalhes
            result = self.driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-datatable/div/div[1]/table/tbody/tr/td[1]/span[2]/span")
            # result.click()
            self.driver.execute_script("arguments[0].click();", result)

            sleep(self.INTERVALO + self.INTERVALO)
        except:
            print("Não foi possível obter o tipo da peça")
            print(n_peca, sys.exc_info()[0])
        return tipo_peca

    def __set_element(self, xpath):
        field = None
        try:
            field_cmp = self.driver.find_element_by_xpath(xpath)
            field = field_cmp.text.replace("\n",";;")
        except:
            pass
        return field

    def __cmp_n_set_element(self, label, i, xpath):
        field = None
        if (self.__compare_label(label, xpath)):
            field = self.__set_element(xpath + """/span""")
            i += 1
        return field, i

    def __compare_label(self, label, xpath):
        try:
            field = self.driver.find_element_by_xpath(xpath)
        except:
            return False
        return label in field.text

    def extrair_mand_internacao(self):
        """
        """
        xpath_base = """/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]"""
        situacao = self.__set_element(xpath_base + """/p[1]/span""")
        num_mandado = self.__set_element(xpath_base + """/p[2]/span""")
        data_exp = self.__set_element(xpath_base + """/p[3]/span""")
        n_processo = self.__set_element(xpath_base + """/p[4]/span""")
        motivo = self.__set_element(xpath_base + """/p[5]/span""")
        nome_magistrado = self.__set_element(xpath_base + """/p[6]/span""")
        orgao_exp = self.__set_element(xpath_base + """/p[7]/span""")
        municipio = self.__set_element(xpath_base + """/p[8]/span""")
        tipificacoes = self.__set_element(xpath_base + """/p-datatable/div/div[1]/table/tbody""")
        outros_nomes = self.__set_element(xpath_base + """/div[4]/table/tbody/tr/td""")
        i = 13
        nacionalidade, i = self.__cmp_n_set_element("Nacionalidade:", i, xpath_base + f"""/p[{i}]""")
        naturalidade, i = self.__cmp_n_set_element("Naturalidade:", i, xpath_base + f"""/p[{i}]""")
        dt_nasc, i = self.__cmp_n_set_element("Data de nascimento(s):", i, xpath_base + f"""/p[{i}]""")
        sexo, i = self.__cmp_n_set_element("Sexo:", i, xpath_base + f"""/p[{i}]""")

        # retorna
        mandado = ["I", situacao, None, data_exp, None, n_processo, None, motivo, nome_magistrado, orgao_exp, municipio, tipificacoes, outros_nomes, nacionalidade, naturalidade, dt_nasc, sexo, None, None, None]
        return mandado

    def extrair_mand_prisao(self):
        """
        """
        xpath_base = """/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]"""

        situacao = self.__set_element(xpath_base + """/p[1]/span""")
        num_mandado = self.__set_element(xpath_base + """/p[2]/span""")
        data_exp = self.__set_element(xpath_base + """/p[3]/span""")
        data_val = self.__set_element(xpath_base + """/p[4]/span""")
        n_processo = self.__set_element(xpath_base + """/p[5]/span""")
        esp_prisao = self.__set_element(xpath_base + """/p[6]/span""")
        nome_magistrado = self.__set_element(xpath_base + """/p[7]/span""")
        orgao_exp = self.__set_element(xpath_base + """/p[8]/span""")
        municipio = self.__set_element(xpath_base + """/p[9]/span""")
        tipificacoes = self.__set_element(xpath_base + """/p-datatable/div/div[1]/table/tbody""")
        outros_nomes = self.__set_element(xpath_base + """/div[4]/table/tbody/tr/td""")

        i = 15
        nacionalidade, i = self.__cmp_n_set_element("Nacionalidade:", i, xpath_base + f"""/p[{i}]""")
        naturalidade, i = self.__cmp_n_set_element("Naturalidade:", i, xpath_base + f"""/p[{i}]""")
        dt_nasc, i = self.__cmp_n_set_element("Data de nascimento(s):", i, xpath_base + f"""/p[{i}]""")
        sexo, i = self.__cmp_n_set_element("Sexo:", i, xpath_base + f"""/p[{i}]""")

        recaptura = self.__set_element(xpath_base + f"""/p[{i}]/span""")
        i += 1
        pena_imposta = self.__set_element(xpath_base + f"""/p[{i}]/span""")
        i += 1
        regime_cump = self.__set_element(xpath_base + f"""/p[{i}]/span""")

        mandado = ["P", situacao, num_mandado, data_exp, data_val, n_processo, esp_prisao, None, nome_magistrado, orgao_exp, municipio, tipificacoes, outros_nomes, nacionalidade, naturalidade, dt_nasc, sexo, recaptura, pena_imposta, regime_cump]
        return mandado
