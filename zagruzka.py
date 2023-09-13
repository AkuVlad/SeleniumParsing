from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from datetime import timedelta
import time
import datetime
#Путь к выходному файлу
file_path = r'C:\Проекты\Step7\Автоматизация отчета по загрузке и выгрузке\report.txt'
#Выходная переменная с текстом, инициализируем
output = ''
#Вводим начальное значение
print('Введите начальную дату и время в формате ГГГГ-ММ-ДД ЧЧ:ММ')
startdate = input()
#Вводим конечное значение
print('Введите конечную дату и время в формате ГГГГ-ММ-ДД ЧЧ:ММ')
enddate = input()
#Преобразовываем значения в объект datetime
startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d %H:%M')
enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d %H:%M')
#Находим разницу во времени и вычисляем число итераций с шагом 30 минут
resolution = timedelta(minutes = 30) #шаг измерения, дискретность
counts = int((enddate - startdate)/resolution)
#настраиваем браузер - указываем местоположение exeшника драйвера и браузера 
options = Options()
options.add_argument("--headless")
options.binary_location = "C:\Проекты\Step7\АвтоматизацияОбходаОкраски\Для мастеров смены\chrome-win64\chrome-win64\chrome.exe"
options.browserName = "Chrome" #"C:\Windows\System32\chromedriver.exe"
service = ChromeService("C:\Windows\System32\chromedriver.exe")
browser = webdriver.Chrome( service = service,options = options)
#Авторизируемся 
browser.get('http://10.246.154.137:8080/gtts/login.jsf')
login = browser.find_element(by=By.NAME, value="formAll:j_id170")
password = browser.find_element(by=By.NAME, value="formAll:j_id172")
submit_password = browser.find_element(by=By.NAME, value="formAll:bt_login")
login.send_keys("vulk")
password.send_keys("123")
submit_password.click()
browser.get('http://10.246.154.137:8080/gtts/auswertungen/einlagerungen.jsf')
time.sleep(1)
#Делаем цикл из следующих действий:
for number in range(counts):
#Меняем даты на нужные нам, предварительно вычислив их
    enddate = startdate + resolution
    browser.execute_script("document.getElementById('uebersichtStoreForm:vonDatumInputDate').setAttribute('value', '"+str(startdate)+"')")
    browser.execute_script("document.getElementById('uebersichtStoreForm:bisDatumInputDate').setAttribute('value', '"+str(enddate)+"')")
    time.sleep(1)
#сохраняем начальную дату итерации
    from_datetime = browser.find_element(by=By.ID, value="uebersichtStoreForm:vonDatumInputDate")
    from_datetime = from_datetime.get_attribute('value')
    time.sleep(1)
#сохраняем конечную дату итерации
    to_datetime = browser.find_element(by=By.ID, value="uebersichtStoreForm:bisDatumInputDate")
    to_datetime = to_datetime.get_attribute('value')
    time.sleep(1)
#Нажимаем на кнопку отчеты
    apply = browser.find_element(by=By.NAME, value="uebersichtStoreForm:j_id175")
    apply.click()
    time.sleep(1)
#Открылась новая вкладка браузера
    browser.switch_to.window(browser.window_handles[1])
    time.sleep(1)
#получаем число страниц поиска 
    page_number = browser.find_element(By.CSS_SELECTOR, 'tr.style_6>td:nth-child(3) > table > tbody > tr>td:nth-child(4) > div')
    pages = page_number.text
#находим поле ввода порядкого номера страницы и записываем туда число
    input_field = browser.find_element(by=By.ID, value="gotoPage")
    input_field.send_keys(pages)
#нажимаем на кнопку перейти на страницу
    page_button = browser.find_element(By.CSS_SELECTOR, '.birtviewer_navbar > tbody > tr:nth-child(2) > td:nth-child(15) > input')
    page_button.click()
    time.sleep(1)
#Записываем число колес
    tire_count = browser.find_element(By.CSS_SELECTOR, 'tr.style_13 > td.style_14:nth-child(2) > div')#Проверить!!!!!
    tire_count = tire_count.text
#Закрываем вкладку и переходим на следующее окно
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    #записываем строку с результатом
    output = output + 'C '+from_datetime+' по '+to_datetime+' загружено -- '+tire_count+' шин, '
    print(output)
######переходим на выгрузку
    browser.get('http://10.246.154.137:8080/gtts/auswertungen/auslagerungen.jsf')
    time.sleep(1)
    browser.execute_script("document.getElementById('uebersichtStoreForm:vonDatumInputDate').setAttribute('value', '"+str(startdate)+"')")
    browser.execute_script("document.getElementById('uebersichtStoreForm:bisDatumInputDate').setAttribute('value', '"+str(enddate)+"')")
    #сохраняем начальную дату итерации
    from_datetime = browser.find_element(by=By.ID, value="uebersichtStoreForm:vonDatumInputDate")
    from_datetime = from_datetime.get_attribute('value')
    time.sleep(1)
#сохраняем конечную дату итерации
    to_datetime = browser.find_element(by=By.ID, value="uebersichtStoreForm:bisDatumInputDate")
    to_datetime = to_datetime.get_attribute('value')
    time.sleep(1)
#Нажимаем на кнопку отчеты
    apply = browser.find_element(by=By.NAME, value="uebersichtStoreForm:j_id175")
    apply.click()
    time.sleep(1)
#Открылась новая вкладка браузера
    browser.switch_to.window(browser.window_handles[1])
    time.sleep(1)
#получаем число страниц поиска 
    page_number = browser.find_element(By.CSS_SELECTOR, 'tr.style_6>td:nth-child(3) > table > tbody > tr>td:nth-child(4) > div')
    pages = page_number.text
#находим поле ввода порядкого номера страницы и записываем туда число
    input_field = browser.find_element(by=By.ID, value="gotoPage")
    input_field.send_keys(pages)
#нажимаем на кнопку перейти на страницу
    page_button = browser.find_element(By.CSS_SELECTOR, '.birtviewer_navbar > tbody > tr:nth-child(2) > td:nth-child(15) > input')
    page_button.click()
    time.sleep(1)
#Записываем число колес
    tire_count = browser.find_element(By.CSS_SELECTOR, '.style_12 > td:nth-child(2)> div')#Проверить!!!!!
    tire_count = tire_count.text
#Закрываем вкладку и переходим на следующее окно
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
#Обновляем значение
    startdate = enddate
#пишем в консоль
    output = output + 'выгружено -- '+tire_count+' шин\n'
    print(output)
#идем обратно на загрузку
    browser.get('http://10.246.154.137:8080/gtts/auswertungen/einlagerungen.jsf')
    time.sleep(1)
f = open(file_path, '+r')
f.truncate(0)
f.write(output)
f.close()
time.sleep(3)