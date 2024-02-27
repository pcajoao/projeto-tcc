from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import csv

#lista de colunas a serem formatadas no arquivo final
res = [['ANO', 'FILTRO', 'CONTEUDO', 'CHAVE', 'VALOR']]

# lista de filtros para linhas organizada por ID
filters_l = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

# lista de filtros para conteudo organizada por ID
filters_i = [1,2]

# lista de filtros para anos organizada por ID
filters_a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
options_name = {}

# inicio do navegador sem cabeçalho
driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--headless=new")
driver = webdriver.Chrome(options=driver_option)

# site alvo
driver.get("http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinasc/cnv/nvuf.def")


# função de rotina para ações de clique na tela durante a navegação
def click_option(filter_option, value):
  filter_element =  driver.find_element(By.XPATH, "//*[@id='%s']" % filter_option)
  select = Select(filter_element)

  if(select.is_multiple):
    select.deselect_all()

  option = driver.find_element(By.XPATH, "//*[@id='%s']/option[%s]" % (filter_option, value))
  options_name[filter_option] = option.text
  option.click()

# função de estruturação dos objetos a serem inseridos na base final
def populate():
  table = driver.find_elements(By.TAG_NAME, "tbody")

  if(len(table) > 0):
    table = table[0]
    trs = table.find_elements(By.TAG_NAME, "tr")

    for tr in trs:
      tds = tr.find_elements(By.TAG_NAME, "td")
      line_content = [options_name["A"], options_name["L"], options_name["I"], tds[0].text, tds[1].text]
      res.append(line_content)
      
# loop de iteração entre os diversos filtros da tela
for l in filters_l:
  for i in filters_i:
    for a in filters_a:
      filters = {"L": l, "I": i, "A": a}
      print(filters)
      filtersKeys = filters.keys()
      
      for option in filtersKeys:
        click_option(option, filters[option])

      btn_open = driver.find_element(By.NAME, "mostre")
      btn_open.click()

      driver.switch_to.window(driver.window_handles[1])

      populate()

      driver.close()
      driver.switch_to.window(driver.window_handles[0])

      temp_res = {}
      options_name = {}

file_name = 'result.csv'

# escrita do arquivo com todos os dados extraidos da pagina alvo
with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(res)

# fim do navegador sem cabeçalho
driver.quit()