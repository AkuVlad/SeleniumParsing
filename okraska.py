from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
options = Options()
options.binary_location = "C:\Проекты\Step7\АвтоматизацияОбходаОкраски\Для мастеров смены\chrome-win64\chrome-win64\chrome.exe"
options.browserName = "Chrome" #"C:\Windows\System32\chromedriver.exe"
service = ChromeService("C:\Windows\System32\chromedriver.exe")
browser = webdriver.Chrome( service = service,options = options) 
browser.get('http://10.246.154.137:8080/gtts/login.jsf')
login = browser.find_element(by=By.NAME, value="formAll:j_id170")
password = browser.find_element(by=By.NAME, value="formAll:j_id172")
submit_password = browser.find_element(by=By.NAME, value="formAll:bt_login")
login.send_keys("vulk")
password.send_keys("123")
submit_password.click()
browser.get('http://10.246.154.137:8080/gtts/bauteilerfassung/palettendaten.jsf')
#нажимаю окраску
painting = WebDriverWait(browser,30).until(EC.presence_of_element_located((By.ID,"formAll:dataTable:id_headerOutputText_dynamic_1")))
painting.click()
time.sleep(0.5)
#нажимаю "обновить"
refresh = WebDriverWait(browser,30).until(EC.presence_of_element_located((By.ID,"formAll:dataTable:cl_aktualisieren")))
refresh.click()
#x - счетчик окрашенных колес
x = 0
#Делаем то что снизу 50 раз
for number in range(70):
    #Нажимаем на первую строку
    first_string = WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CLASS_NAME,"rich-table-firstrow")))
    first_string.click()
    #Ставим галочку
    checkbox = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,"formAll:id_in_panel_dynamic_1")))
    state = checkbox.is_selected()
    state = str(state)
    print('Состояние галочки на окраске до работы программы - '+state)
    #Нажимаем подтвердить если галочка не проставлена
    if state == 'False':
        checkbox.click()
        state2 = checkbox.is_selected()
        print('После клика состояние - '+str(state2))
        submit_painting = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.NAME,"formAll:j_id174")))
        submit_painting.click()
        time.sleep(0.2)
        x += 1
        print('>>>>>>>>>>Всего проставлено '+str(x)+' колес<<<<<<<<<<<<<<<')
    #иначе завершить программу
    else:
         print('Прерываем выполнение')
         exit()    


