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
        self.driver = webdriver.Chrome() if not driver else driver
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
        dropdown = self.driver.find_element_by_xpath("//p-dropdown[@name='idEstado']")
        dropdown.click()

        # Obtém o input
        cmp_input = dropdown.find_elements_by_xpath(""".//input""")[-1]  # Encontra todos os inputs dentro de
                                                                          # dropdown e seleciona o desejado.
        
        # Primeiro deleta o texto que estiver no campo
        cmp_input.clear()
        
        sleep(self.INTERVALO)
        
        # Envia o nome da UF para o campo
        cmp_input.send_keys(uf)
        
        sleep(self.INTERVALO)

        # Seleciona o estado resultante
        cmp_li = dropdown.find_element_by_xpath("//*[@class='ui-dropdown-items-wrapper']/ul/li")

        # Clica no pesquisar do estado para preencher com o nome
        cmp_li.click()
        
        sleep(self.INTERVALO)

        botão_pesq = self.driver.find_element_by_xpath("//button[@label='Pesquisar']")
        botão_pesq.click()
        
        sleep(self.INTERVALO)
                
        btn_1a_pag = self.driver.find_element_by_class_name("ui-paginator-first")
        if (self.__btn_esta_habilitado(btn_1a_pag)):
            btn_1a_pag.click()
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
                    mandado = ["ERRO"]
                #mandado.insert(0, num_peca)
                mandado.insert(0, UF)
                self.mandados.append(mandado)
        self.to_tsv()
    
    def to_tsv(self, sep='\t'):
        nomes_cols = ["UF", "Tipo Mandado", "Situacao", "Número Mandado", "Data de Expedição", "Data de Validade", "Número Processo", "Espécie de Prisão", "Nome Magistrado", "Órgão Expedidor", "Munícipio", "Tipificações Penais", "Nome", "Nacionalidade", "Naturalidade", "Data Nascimento", "Sexo", "Recaptura", "Pena Imposta", "Regime"]
        df = pd.DataFrame(self.mandados, columns=[nomes_cols])
        df.to_csv('mandados.tsv', sep=sep)
        
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
    
    def extrair_mand_internacao(self):
        """
        """
        
        try:
            situacao_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[1]/span""")
            situacao = situacao_cmp.text.replace("\n",";;")
        except:
            situacao = ""
        # num mandado de internação
        try:
            num_mandado_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[2]/span""")
            num_mandado = num_mandado_cmp.text.replace("\n",";;")
        except:
            num_mandado = ""
        # campo data exp
        try:
            data_exp_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[3]/span""")
            data_exp = data_exp_cmp.text.replace("\n",";;")
        except:
            data_exp = ""
        # campo n processo
        try:
            n_processo_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[4]/span""")
            n_processo = n_processo_cmp.text.replace("\n",";;")
        except:
            n_processo = ""
        # motivo internação
        try:
            motivo_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[5]/span""")
            motivo = motivo_cmp.text.replace("\n",";;")
        except:
            motivo = ""
        # campo nome magistrado
        try:
            nome_magistrado_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[6]/span""")
            nome_magistrado = nome_magistrado_cmp.text.replace("\n",";;")
        except:
            nome_magistrado = ""
        # campo orgão exp
        try:
            orgao_exp_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[7]/span""")
            orgao_exp = orgao_exp_cmp.text.replace("\n",";;")
        except:
            orgao_exp = ""
        # campo municipio
        try:
            municipio_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[8]/span""")
            municipio = municipio_cmp.text.replace("\n",";;")
        except:
            municipio = ""
        # campo tipificacoes
        try:
            tipificacoes_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-72-content"]/div[1]/p-datatable/div/div[1]/table""")
            tipificacoes = tipificacoes_cmp.text.replace("\n",";;")
        except:
            tipificacoes = ""
        # campo outros nomes
        try:
            outros_nomes_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/div[4]/table/tbody/tr[1]/td""")
            outros_nomes = outros_nomes_cmp.text.replace("\n",";;")
        except:
            outros_nomes = ""
        # nacionalidade
        try:
            nacionalidade_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[12]/span/span""")
            nacionalidade = nacionalidade_cmp.text.replace("\n",";;")
        except:
            nacionalidade = ""
        # naturalidade
        try:
            naturalidade_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[13]/span/span""")
            naturalidade = naturalidade_cmp.text.replace("\n",";;")
        except:
            naturalidade = ""
        # campo dt nasc
        try:
            dt_nasc_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[14]/span/span""")
            dt_nasc = dt_nasc_cmp.text.replace("\n",";;")
        except:
            dt_nasc = ""
        # campo sexo
        try:
            sexo_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-71-content"]/div[1]/p[15]/span""")
            sexo = sexo_cmp.text.replace("\n",";;")
        except:
            sexo = ""
            
        # retorna
        mandado = ["Internação", situacao, "", data_exp, "", n_processo, "", nome_magistrado, orgao_exp, municipio, tipificacoes, outros_nomes, "", "", dt_nasc, sexo, "", "", ""]
        print(mandado)
        return mandado

    def extrair_mand_prisao(self):
        """
        """
        
        try:
            situacao_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[1]/span""")
            situacao = situacao_cmp.text.replace("\n",";;")
        except:
            situacao = ""
        # numero do mandado de prisão
        try:
            n_mandado_prisao_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[2]/span""")
            n_mandado_prisao = n_mandado_prisao_cmp.text.replace("\n", ";;")
        except:
            n_mandado_prisao = ""
        # campo data expedicao
        try:
            data_exp_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[3]/span""")
            data_exp = data_exp_cmp.text.replace("\n",";;")
        except:
            data_exp = ""
        # campo data de validade
        try:
            data_val_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[4]/span""")
            data_val = data_val_cmp.text.replace("\n",";;")
        except:
            data_val = ""
        # campo n processo
        try:
            n_processo_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[5]/span""")
            n_processo = n_processo_cmp.text.replace("\n",";;")
        except:
            n_processo = ""
        # especie de prisao
        try:
            esp_prisao_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[6]/span""")
            esp_prisao = esp_prisao_cmp.text.replace("\n",";;")
        except:
            esp_prisao = ""
        # campo nome magistrado
        try:
            nome_magistrado_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[7]/span""")
            nome_magistrado = nome_magistrado_cmp.text.replace("\n",";;")
        except:
            nome_magistrado = ""
        # campo orgão exp
        try:
            orgao_exp_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[8]/span""")
            orgao_exp = orgao_exp_cmp.text.replace("\n",";;")
        except:
            orgao_exp = ""
        # campo municipio
        try:
            municipio_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[9]/span""")
            municipio = municipio_cmp.text.replace("\n",";;")
        except:
            municipio = ""
        # campo tipificacoes
        try:
            tipificacoes_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p-datatable/div/div[1]/table""")
            tipificacoes = tipificacoes_cmp.text.replace("\n",";;")
        except:
            tipificacoes = ""
        # campo outros nomes
        try:
            outros_nomes_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/div[4]/table/tbody/tr/td""")
            outros_nomes = outros_nomes_cmp.text.replace("\n",";;")
        except:
            outros_nomes = ""
        # nacionalidade
        try:
            nacionalidade_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[14]/span""")
            nacionalidade = nacionalidade_cmp.text.replace("\n",";;")
        except:
            nacionalidade = ""
        # naturalidade
        try:
            naturalidade_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[15]/span""")
            naturalidade = naturalidade_cmp.text.replace("\n",";;")
        except:
            naturalidade = ""
        # campo dt nasc
        try:
            dt_nasc_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[16]/span/span""")
            dt_nasc = dt_nasc_cmp.text.replace("\n",";;")
        except:
            dt_nasc = ""
        # campo sexo
        try:
            sexo_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[17]/span""")
            sexo = sexo_cmp.text.replace("\n",";;")
        except:
            sexo = ""
        # Recaptura
        try:
            recaptura_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[18]/span""")
            recaptura = recaptura_cmp.text.replace("\n",";;")
        except:
            recaptura = ""
        # pena imposta
        try:
            pena_imposta_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[19]/span""")
            pena_imposta = pena_imposta_cmp.text.replace("\n",";;")
        except:
            pena_imposta = ""
        # regime de cumprimento
        try:
            regime_cump_cmp = self.driver.find_element_by_xpath("""//*[@id="ui-panel-73-content"]/div[1]/p[20]/span""")
            regime_cump = regime_cump_cmp.text.replace("\n",";;")
        except:
            regime_cump = ""
            
        mandado = ["Prisão", situacao, n_mandado_prisao, data_exp, data_val, n_processo, esp_prisao, nome_magistrado, orgao_exp, municipio, tipificacoes, outros_nomes, nacionalidade, naturalidade, dt_nasc, sexo, recaptura, pena_imposta, regime_cump]
        print(mandado)
        return mandado

    def fechar_driver(self):
        self.driver.quit()