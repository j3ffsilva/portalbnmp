from ExtratorBNMP import *  # Para obter tudo que foi definido no ExtratorBNMP.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Para salvar alguns arquivos do navegador localmente e então evitar a necessidade
# de se passar pelo captcha toda vez que se roda o programa
chrome_options = Options()
chrome_options.add_argument("user-data-dir=driverdata")
caminho_driver = COLOQUE AQUI O CAMINHO DO SEU CHROMEDRIVER ENTRE ASPAS
# Ps. se você costuma não precisar colocar o caminho do seu chromedriver pode apagar
# a linha acima e também tirar o 'caminho_driver' do próximo comando

# Deninindo o driver
driver = webdriver.Chrome(caminho_driver, options=chrome_options)

# Criando uma instância da nossa classe
extrator = ExtratorBNMP(driver=driver, raspar_1a_pag=True)

# Exemplo de uso
extrator.selecionar_UF("Acre")
