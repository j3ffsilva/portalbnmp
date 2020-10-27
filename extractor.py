#_*_coding: utf-8_*_
#! usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from acre import f_acre
import sys

def obter_driver():
    driver = webdriver.Firefox()
    return driver

def iniciar(driver):
    driver.get("https://portalbnmp.cnj.jus.br/")

def extrair_mand_internacao(driver):
    try:
        situacao_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[1]/span")
        situacao = situacao_cmp.text.replace("\n",";;")
    except:
        situacao = ""
    # num mandado de internação
    try:
        num_mandado_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[2]/span")
        num_mandado = num_mandado_cmp.text.replace("\n",";;")
    except:
        num_mandado = ""
    # campo data exp
    try:
        data_exp_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[3]/span")
        data_exp = data_exp_cmp.text.replace("\n",";;")
    except:
        data_exp = ""
    # campo n processo
    try:
        n_processo_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[4]/span")
        n_processo = n_processo_cmp.text.replace("\n",";;")
    except:
        n_processo = ""
    # motivo internação
    try:
        motivo_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[5]/span")
        motivo = motivo_cmp.text.replace("\n",";;")
    except:
        motivo = ""
    # campo nome magistrado
    try:
        nome_magistrado_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[6]/span")
        nome_magistrado = nome_magistrado_cmp.text.replace("\n",";;")
    except:
        nome_magistrado = ""
    # campo orgão exp
    try:
        orgao_exp_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[7]/span")
        orgao_exp = orgao_exp_cmp.text.replace("\n",";;")
    except:
        orgao_exp = ""
    # campo municipio
    try:
        municipio_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[8]/span")
        municipio = municipio_cmp.text.replace("\n",";;")
    except:
        municipio = ""
    # campo tipificacoes
    try:
        tipificacoes_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p-datatable/div/div[1]/table")
        tipificacoes = tipificacoes_cmp.text.replace("\n",";;")
    except:
        tipificacoes = ""
    # campo outros nomes
    try:
        outros_nomes_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/div[4]/table")
        outros_nomes = outros_nomes_cmp.text.replace("\n",";;")
    except:
        outros_nomes = ""
    # nacionalidade
    try:
        nacionalidade_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[14]/span")
        nacionalidade = nacionalidade_cmp.text.replace("\n",";;")
    except:
        nacionalidade = ""
    # naturalidade
    try:
        naturalidade_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[15]/span")
        naturalidade = naturalidade_cmp.text.replace("\n",";;")
    except:
        naturalidade = ""
    # campo dt nasc
    try:
        dt_nasc_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[14]/span/span")
        dt_nasc = dt_nasc_cmp.text.replace("\n",";;")
    except:
        dt_nasc = ""
    # campo sexo
    try:
        sexo_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[15]/span")
        sexo = sexo_cmp.text.replace("\n",";;")
    except:
        sexo = ""
    # retorna
    return ["Internação", situacao, data_exp, n_processo, nome_magistrado, orgao_exp, municipio, tipificacoes, outros_nomes, dt_nasc, sexo]

def extrair_mand_prisao(driver):
    try:
        situacao_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[1]/span")
        situacao = situacao_cmp.text.replace("\n",";;")
    except:
        situacao = ""
    # numero do mandado de prisão
    try:
        n_mandado_prisao_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[2]/span")
        n_mandado_prisao = n_mandado_prisao_cmp.text.replace("\n", ";;")
    except:
        n_mandado_prisao = ""
    # campo data expedicao
    try:
        data_exp_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[3]/span")
        data_exp = data_exp_cmp.text.replace("\n",";;")
    except:
        data_exp = ""
    # campo data de validade
    try:
        data_val_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[4]/span")
        data_val = data_val_cmp.text.replace("\n",";;")
    except:
        data_val = ""
    # campo n processo
    try:
        n_processo_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[5]/span")
        n_processo = n_processo_cmp.text.replace("\n",";;")
    except:
        n_processo = ""
    # especie de prisao
    try:
        esp_prisao_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[6]/span")
        esp_prisao = esp_prisao_cmp.text.replace("\n",";;")
    except:
        esp_prisao = ""
    # campo nome magistrado
    try:
        nome_magistrado_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[7]/span")
        nome_magistrado = nome_magistrado_cmp.text.replace("\n",";;")
    except:
        nome_magistrado = ""
    # campo orgão exp
    try:
        orgao_exp_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[8]/span")
        orgao_exp = orgao_exp_cmp.text.replace("\n",";;")
    except:
        orgao_exp = ""
    # campo municipio
    try:
        municipio_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[9]/span")
        municipio = municipio_cmp.text.replace("\n",";;")
    except:
        municipio = ""
    # campo tipificacoes
    try:
        tipificacoes_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p-datatable/div/div[1]/table")
        tipificacoes = tipificacoes_cmp.text.replace("\n",";;")
    except:
        tipificacoes = ""
    # campo outros nomes
    try:
        outros_nomes_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/div[4]/table")
        outros_nomes = outros_nomes_cmp.text.replace("\n",";;")
    except:
        outros_nomes = ""
    # nacionalidade
    try:
        nacionalidade_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[14]/span")
        nacionalidade = nacionalidade_cmp.text.replace("\n",";;")
    except:
        nacionalidade = ""
    # naturalidade
    try:
        naturalidade_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[15]/span")
        naturalidade = naturalidade_cmp.text.replace("\n",";;")
    except:
        naturalidade = ""
    # campo dt nasc
    try:
        dt_nasc_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[16]/span/span")
        dt_nasc = dt_nasc_cmp.text.replace("\n",";;")
    except:
        dt_nasc = ""
    # campo sexo
    try:
        sexo_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[17]/span")
        sexo = sexo_cmp.text.replace("\n",";;")
    except:
        sexo = ""
    # Recaptura
    try:
        recaptura_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[18]/span")
        recaptura = recaptura.text.replace("\n",";;")
    except:
        recaptura = ""
    # pena imposta
    try:
        pena_imposta_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[19]/span")
        pena_imposta = pena_imposta_cmp.text.replace("\n",";;")
    except:
        pena_imposta = ""
    # regime de cumprimento
    try:
        regime_cump_cmp = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-resumo-peca/div/p-panel/div/div[2]/div[1]/p[20]/span")
        regime_cump = regime_cump_cmp.text.replace("\n",";;")
    except:
        regime_cump = ""
    # retorna
    return ["Prisão", situacao, n_mandado_prisao, data_exp, data_val, n_processo, esp_prisao, nome_magistrado, orgao_exp, municipio, tipificacoes, outros_nomes, nacionalidade, naturalidade, dt_nasc, sexo, recaptura, pena_imposta, regime_cump]

def detalhar(n_peca, driver):
    # Encontra e preenche o numero da peça
    cmp_pesq_xpath = "/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-fieldset/fieldset/div/div/form/div[9]/span/p-inputmask/input"
    cmp_pesquisa = driver.find_element_by_xpath(cmp_pesq_xpath)
    time.sleep(0.5)
    cmp_pesquisa.send_keys(n_peca)
    time.sleep(0.5)
    # Encontra e clica no botão de pesquisar
    button_pesq = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-fieldset/fieldset/div/div/form/div[14]/button[2]")
    button_pesq.click()
    time.sleep(1)
    # tipo peca
    tipo_peca = None
    try:
        tipo_peca_xpath = "/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-datatable/div/div[1]/table/tbody/tr/td[6]/span[2]"
        tipo_peca_cmp = driver.find_element_by_xpath(tipo_peca_xpath)
        tipo_peca = tipo_peca_cmp.text
        # Clica no processo de retorno
        result = driver.find_element_by_xpath("/html/body/app-root/div/div/div[2]/div/app-pesquisa-peca/div[1]/p-datatable/div/div[1]/table/tbody/tr/td[1]/span[2]/span")
        result.click()
    except:
        print("Não foi possível obter o tipo da peça")
        print(n_peca, sys.exc_info()[0])
    return tipo_peca

def rodar(driver, filename, f):
    # n_pecas = f_acre()
    n_pecas = f()
    total = len(n_pecas)
    k = 0
    with open(filename, 'w') as file:
        for num_peca in n_pecas:
            k += 1
            print("=> Processando {} de {}".format(k, total))
            try:
                iniciar(driver)
                time.sleep(0.5)
                tipo_peca = detalhar(num_peca, driver)
                time.sleep(0.5)
                mandado = None
                if (tipo_peca == "Mandado de Internação"):
                    mandado = extrair_mand_internacao(driver)
                elif (tipo_peca == "Mandado de Prisão"):
                    mandado = extrair_mand_prisao(driver)
                else:
                    mandado = ["ERRO"]
                mandado.insert(0, num_peca)
                file.write("\t".join(mandado))
            except:
                print(num_peca, sys.exc_info()[0])
                file.write("\t".join([num_peca,"[ERRO]"]))
            file.write("\n")

def f_amostra():
    return ["0004396-57.2016.8.01.0001.10.0001-25", "0012284-14.2015.8.01.0001.10.0001-15", "0000393-52.2018.8.01.0013.01.0003-25", "0000019-72.2018.8.01.0001.01.0001-01", "0000179-61.2018.8.01.0013.01.0003-06", "0001661-13.2000.8.01.0001.01.0001-08", "0007219-48.2009.8.01.0001.01.0001-16", "0001731-62.2016.8.01.0003.01.0001-00", "0019498-03.2008.8.01.0001.01.0001-16", "0024192-78.2009.8.01.0001.01.0001-04", "0704568-21.2017.8.01.0001.01.0001-13", "0704208-86.2017.8.01.0001.01.0001-27", "0700894-06.2015.8.01.0001.01.0001-21", "0000347-73.2007.8.01.0005.01.0005-10", "0018960-17.2011.8.01.0001.01.0001-20", "0002031-84.2003.8.01.0001.01.0001-04", "0001694-66.2001.8.01.0001.01.0001-01", "0013697-14.2005.8.01.0001.01.0001-03", "0200196-92.2008.8.01.0004.01.0001-13", "0006039-12.2000.8.01.0001.01.0001-17", "0015253-27.2000.8.01.0001.01.0001-13", "0003231-47.2013.8.01.0011.01.0001-20", "0000480-92.2010.8.01.0011.01.0001-15"]

# Para executar o script, rode diretamente em um shell:
driver = obter_driver()
iniciar(driver)
# Roda tudo do acre (dia 21-10-2020)
rodar(driver, 'acre.tsv', f_acre)

# Roda tudo na amostra
rodar(driver, 'amostra.tsv', f_amostra)
