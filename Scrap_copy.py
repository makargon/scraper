from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from base64 import b64decode
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract

import os.path
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


# prox = Proxy()
# prox.proxy_type = ProxyType.MANUAL
# prox.http_proxy = "ip_addr:port"
# prox.socks_proxy = "ip_addr:port"
# prox.ssl_proxy = "ip_addr:port"

# capabilities = webdriver.DesiredCapabilities.CHROME
# prox.add_to_capabilities(capabilities)

class Scrap():
    city = "Москва"
    searchMode = True  # True: точный, False: категории
    searchText = "Автомобили"
    category = "Автомобили"
    pages = 1  # кол-во страниц поиска
    mode = True  # True: объявления, False: обзвон

    checkPhone = True
    checkAllViews = True
    checkDayViews = True
    checkPiar = True
    stoping = False
    url = ''

    # ----------------Google API------------
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # If modifying these scopes, delete the file token.json.

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1-iwN06uZH2I2KkBrHjuzPdkgd4V3GnU8vAS2kMg1tCE'
    SAMPLE_RANGE_NAME = 'Sheet1'

    service = build(
        'sheets', 'v4', credentials=credentials).spreadsheets().values()

    # Call the Sheets API
    #sheet = service.spreadsheets()
    # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    # range=SAMPLE_RANGE_NAME).execute()
    #values = result.get('values', [])

    result_list = []
    list1 = [result_list]

    # ------------Методы----------------
    def clear_the_table(self):
        self.range_ = "Sheet1!A1:Z1000"
        self.response = self.service.clear(
            spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range=self.range_).execute()

    def openBrowser(self):
        self.options = webdriver.ChromeOptions()
        pytesseract.pytesseract.tesseract_cmd = 'Tesseract\\tesseract.exe'
        # Пропишите здесь свой юзер агент. в формате "user-agent="
        ua = "user-agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        cookie = 'cookie=u=2tkt0i5t.14ibcxl.sku9ymz5wqw0; buyer_laas_location=646600; buyer_location_id=646600; _gcl_au=1.1.1934383239.1668324089; _ym_uid=1668324093928191202; _ym_d=1668324093; tmr_lvid=74af42bd79ebf0d390a55ef90dddae0c; tmr_lvidTS=1668324099764; uxs_uid=d77aae20-6323-11ed-8adb-a36376a09f25; adrcid=AN_Pao7fiN9RNcNM2HdsP-A; __zzatw-avito=MDA0dBA=Fz2+aQ==; __zzatw-avito=MDA0dBA=Fz2+aQ==; auth=1; _gid=GA1.2.535908346.1668346027; _ga=GA1.1.188925168.1668324094; cfidsw-avito=2Vf0a0kI1uLj5P5YFXlbLTVWVNtvQJUgHIe9Z6kvsNm9TTT4V1n7dbU05dvfwt4h724JL0FkNmhDhdHiwdTZlp0XD74MZ04Y9llglq8wzveOywHqw++ifO55XRz0FkgbllN7InE2STH41ZEjUc9En6B/0pI4MA90yO7p+w==; cfidsw-avito=2Vf0a0kI1uLj5P5YFXlbLTVWVNtvQJUgHIe9Z6kvsNm9TTT4V1n7dbU05dvfwt4h724JL0FkNmhDhdHiwdTZlp0XD74MZ04Y9llglq8wzveOywHqw++ifO55XRz0FkgbllN7InE2STH41ZEjUc9En6B/0pI4MA90yO7p+w==; gsscw-avito=WAX0Jl8neymOBh5WkXCM/gcmIe3kNsuq0OHzgStLhZCrvesb2uxCf4QFun/YPtdvhsLR92dM9wihkEniFyqwIGVwU7t6g/wg9haAmVJaIn616zBWcZg5anaAhtaHgFitvoSOEVbHEzCzf5vDgs80q3HVsIySnWRFIqAmrguSZ8I8xalLYm6YZofRHcY2+WJfQvIFOiDHz7ja1tbACVv5+Qrk9Z2lPSyN7eDf/SqQ/iFQV9X2eYe1oMBE5w4Jt3di; gsscw-avito=WAX0Jl8neymOBh5WkXCM/gcmIe3kNsuq0OHzgStLhZCrvesb2uxCf4QFun/YPtdvhsLR92dM9wihkEniFyqwIGVwU7t6g/wg9haAmVJaIn616zBWcZg5anaAhtaHgFitvoSOEVbHEzCzf5vDgs80q3HVsIySnWRFIqAmrguSZ8I8xalLYm6YZofRHcY2+WJfQvIFOiDHz7ja1tbACVv5+Qrk9Z2lPSyN7eDf/SqQ/iFQV9X2eYe1oMBE5w4Jt3di; sessid=c3693c45f2df9638334f84317f37908f.1668346956; cfidsw-avito=6IHkEVA8ilBAMUKSJ4Il6d/yZxySiisVFkDb/C/JPP+lg9C9qYWIxTQWoxhLO5FGzunkIuOxs/q3mlRo9SLpwEU8oeJaqrYpW3iV3r9slEwgQWCy4m85dR0cFUGZ4//2aG/PcmNXFyoGjXAv8s6Y6tOjb/9JKqbP7Xu3hw==; fgsscw-avito=gvWYf872097dd8329e6cf3933b001f70cdbb8fc6; fgsscw-avito=gvWYf872097dd8329e6cf3933b001f70cdbb8fc6; _ym_isad=1; f=5.32e32548b6f3e9784b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8068fd850112c943dbcc8809df8ce07f640e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0ac2da10fb74cac1eab268a7bf63aa148d2dc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab71e7cb57bbcb8e0f2da10fb74cac1eab2da10fb74cac1eab0df103df0c26013a037e1fbb3ea05095de87ad3b397f946b4c41e97fe93686adb7ce3c4a759419ab89d2b51f3f3838d502c730c0109b9fbbc60ec9d2f66a8631c9fbdd7f5877c6d729aa4cecca288d6bd7cc8d7ed346c0849bbe0e6a67899bf346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7ac4c51f6e36372136384c864e8cb2503512da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a8134ecdeb26beb8b53778cee096b7b985bf37df0d1894b088; ft="uJp46jv4ST6iqxmiBmoJzMMGlndxKHp75QfXMagbhWFj6Bhr4tL2mbC/ye2ghpFw1m81AgZheFqqEmQNcdTKJ94RfLY5duBdbwhC8yGsRX4DxZgSlM/9ucSo1Un8Vk/XeB5N6CUo01tip4Nkl9QLEbTWmOr+QCKBF2C/gOuZ0TZETR7qsruV2qRSECl07Hz6"; _ga_WW6Q1STJ8M=GS1.1.1668425858.4.1.1668426195.0.0.0; luri=ufa; v=1668427392; isCriteoSetNew=true; _ym_visorc=b; _buzz_fpc=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyVHVlJTJDJTIwMTQlMjBOb3YlMjAyMDIzJTIwMTIlM0EzOCUzQTM3JTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnZhbHVlJTVDJTIyJTNBJTVDJTIyYTVjMzg0OGQwMGVjYWNlNTA3MWVhOWJjNTQwYmNhMTYlNUMlMjIlMkMlNUMlMjJmcGpzRm9ybWF0JTVDJTIyJTNBdHJ1ZSU3RCUyMiU3RA==; sx=H4sIAAAAAAAC/5zQTfLiIBBA8buwzoKPpun2NqGB/COa6GAko5W7T83CGtdzgV/Ve2+FiCgpYGFkj4CcQ8yOU/BaJCRWp7d6qpM6rzEv5Kjt7lGX+xjW5Sx8u8Q87StkNaisTgaRvEFkPAaFLHj3bZujXkEIaK0rdJH2IRM/9v5z39vtZ0m5/J7iJOwv11eri31e/5HggK09BhVKdiZ6KxHHEMhosMTsYaRUIqH7D9k5H45Bcb2Uut3mLfcuTcvUGnUQXT8kmNzniPLiuDsx6Ve5nrfg19g9Yn59k4bD3/5xnOVhFq13aQJdA9WpUgP4kAQ6JfKAHEijHaVETS4bMd6G4tFh1CzOfb+1muk4/gQAAP//Lsyp3rcBAAA=; dfp_group=45; isLegalPerson=0; abp=0; cto_bundle=lz1ThF9tQ0IwbEN6YXluaTdBUEw3RUZLTU5wJTJCaUNLdUhHdFFJWSUyQmxtM25mdWR3MUg0ZVdkdmlDdk8xTFh1RktZTFJKaiUyQmJnVGlKWHFxTnZ1eXhQNk5KNENjSEwyZDBUWm9ZRmZzWndSJTJGU3VBc1JVWm9UM1B0ZlVjOXdnaWJZZWQyNVYlMkJDdDdaV0l4bWRBdHRoUXh0T2tVdjNnJTNEJTNE; _ga_M29JC28873=GS1.1.1668428261.8.1.1668430445.60.0.0; _ga_9E363E7BES=GS1.1.1668428261.7.1.1668430445.60.0.0; tmr_detect=0|1668430450489; tmr_reqNum=245'
        self.options.add_argument(ua)
        self.options.add_argument(cookie)
        with open('config.txt', 'r') as file:
            a = file.readline()
            if a != "":
                self.proxy = '---proxy-server='
                self.proxy += str(a)
                self.options.add_argument(self.proxy)
                print(self.proxy)
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome(options=self.options, service=Service(
            ChromeDriverManager().install()))
        self.driver.get(url="https://www.avito.ru")

        with open('Categoryy.csv', 'r', newline='', encoding='cp866') as self.csvfile:
            self.reader = csv.reader(self.csvfile, delimiter=';', )
            self.dictionary = dict()
            for x in self.reader:
                self.dictionary[x[0]] = x[1]

    def stop(self):  # TODO: переписать
        self.driver.close()
        # self.driver.quit()
        self.stoping = True
        self.driver.get(url="https://www.avito.ru")

    def closeBrowser(self):
        self.driver.close()
        self.driver.quit()

    def search(self):
        self.url = "https://www.avito.ru/ufa?cd=1&q="
        self.searchText = self.searchText.replace(' ', '+')
        self.url += self.searchText

    def adds_analyze(self):
        self.range_ = "Sheet1!A1:Z1000"
        # self.url = "https://www.avito.ru/ufa/avtomobili?cd=1&radius=200"
        self.url = "https://www.avito.ru/kazan/kvartiry"

        if self.searchMode:
            self.search()
            print('searchMode(T): ', self.searchMode)
        else:
            self.url = self.dictionary[self.category]
            print('searchMode(F): ', self.searchMode)
        print('url: ', self.url)
        self.stoping = False

        # for self.x in range(1, ((int(self.pages)+1))):
        if True:
            if self.stoping:
                # self.stoping=False
                print("Парсер остановлен")
                self.driver.get(url="https://www.avito.ru")
                return
            try:
                self.driver.get(url=self.url)
                # login_button = driver.find_element(
                # By.CSS_SELECTOR, "[data-marker='header/login-button']")
                # login_button.click()
                # driver.implicitly_wait(10)
                # log_button = driver.find_element(
                # By.CSS_SELECTOR, "[data-marker='login-form/login']")
                # log_button.send_keys("79061071451")
                # password_button = driver.find_element(
                # By.CSS_SELECTOR, "[data-marker='login-form/password']")
                # password_button.send_keys("16031984@Dd")
                # confirm_button = driver.find_element(
                # By.CSS_SELECTOR, '[data-marker="login-form/submit"]')
                # confirm_button.click()
                # time.sleep(60)
                try:
                    self.location_form = self.driver.find_element(
                        By.CSS_SELECTOR, '[data-marker="search-form/region"]')
                    self.location_form.click()
                    sleep(1)  # 2
                    self.location_input = self.driver.find_element(
                        By.CLASS_NAME, "suggest-input-rORJM")
                    self.location_input.click()
                    self.location_input.send_keys(self.city)
                    sleep(3)  # 5
                    try:
                        self.first_reuslt = self.driver.find_element(
                            By.CSS_SELECTOR, '[data-marker="suggest(0)"]')
                        self.first_reuslt.click()
                    except:
                        print("Не правильный поиск локации")
                    finally:
                        sleep(2)  # 5
                        self.confirm = self.driver.find_element(
                            By.CSS_SELECTOR, '[data-marker="popup-location/save-button"]')

                        self.confirm.click()
                except Exception as ex:
                    print(ex)
                for self.x in range(1, ((int(self.pages)+1))):
                    self.ads = self.driver.find_elements(
                        By.CLASS_NAME, 'iva-item-root-_lk9K')
                    self.piar_list = {}

                    for self.ad in self.ads:
                        if self.stoping:
                            print("Парсер остановлен")
                            self.driver.get(url="https://www.avito.ru")
                            return
                        try:
                            self.arrow = self.ad.find_element(
                                By.CLASS_NAME, "styles-arrow-jfRdd")
                            self.hover = ActionChains(self.driver).move_to_element(
                                self.arrow).perform()
                            sleep(1)  # 2
                            self.piar_data = self.driver.find_elements(
                                By.CLASS_NAME, "styles-entry-MuP_G")

                            self.piar_list.clear
                            for self.piar in self.piar_data:
                                self.piar_text = self.piar.find_element(
                                    By.CLASS_NAME, "styles-title-nWv6g").text
                                self.piar_image = self.piar.find_element(
                                    By.CLASS_NAME, "style-image-wPviB").get_attribute("src")
                                self.spliter = self.piar_image.split(
                                    "https://www.avito.st/s/common/components/monetization/icons/web/")[1]
                                self.piar_orders = self.spliter.replace(
                                    ".svg", "")

                                if len(self.piar_data) == 0:
                                    self.piar_list = "Не использовано услуг продвижения"
                                else:
                                    if "_1" in self.piar_orders:

                                        self.piar_list[self.piar_text] = self.piar_orders
                                    else:
                                        self.piar_list[self.piar_text] = "True"
                                    self.strings = []
                                for self.key, self.item in self.piar_list.items():
                                    self.strings.append("{}: {}".format(
                                        self.key.capitalize(), self.item))
                                self.piar_uslugi = "; ".join(self.strings)
                                self.strings.clear()
                        except Exception as ex:
                            print(ex)
                            self.piar_uslugi = "Не использовано услуг продвижения"
                        sleep(2)  # 3
                        self.ads2 = self.ad.find_element(
                            By.CLASS_NAME, "iva-item-title-py3i_")

                        self.ads2.click()
                        self.driver.implicitly_wait(5)
                        self.driver.switch_to.window(
                            self.driver.window_handles[1])
                        sleep(3)  # 5

                        try:
                            self.title = self.driver.find_element(
                                By.XPATH, "//span[@data-marker='item-view/title-info']").text

                        except:
                            self.title = "Не удалось получить название объявления"

                        self.url = self.driver.current_url
                        try:
                            self.price = self.driver.find_element(
                                By.CLASS_NAME, "style-item-price-text-_w822").text

                        except:
                            self.price = "Не удалось определить цену"

                        try:
                            self.username = self.driver.find_element(
                                By.XPATH, "//div[@data-marker='seller-info/name']").text

                        except:
                            self.username = "Не удалось определить имя пользователя"

                        try:

                            self.location = self.driver.find_element(
                                By.CLASS_NAME, "style-item-address__string-wt61A").text
                        except:
                            self.location = "Не получилось определить адресс"
                        try:
                            self.score = self.driver.find_element(
                                By.CLASS_NAME, "style-seller-info-rating-score-C0y96").text
                        except:
                            self.score = "У пользователя нет рейтинга"
                        try:
                            self.reviews = self.driver.find_element(
                                By.XPATH, "//span[@data-marker='rating-caption/rating']").text
                        except:
                            self.reviews = "У пользователя нет отзывов"
                        try:
                            self.describe = self.driver.find_element(
                                By.XPATH, "//div[@data-marker='item-view/item-description']").text
                        except:
                            self.describe = "Не удалось получить описание товара"
                        try:
                            self.since = self.driver.find_elements(
                                By.CLASS_NAME, "style-seller-info-value-vOioL")[1].text
                        except:
                            self.since = "Не удалось определить с какого времени продавец на авито"
                        # try:
                            # button = driver.find_element(
                            # By.CSS_SELECTOR, '[data-marker="item-phone-button/card"]')
                            # button.click()
                            # phone_number = driver.find_element(
                            # By.CLASS_NAME, "item-popup-itemPhone__img-UxE8p").get_attribute#("src")

                        # except Exception as _ex:
                            # print(_ex)
                            #phone_number = "Не удалось получить номер телефона"
                        try:
                            self.total_views = self.driver.find_element(
                                By.CSS_SELECTOR, '[data-marker="item-view/total-views"]').text
                        except Exception as _ex:
                            print(_ex)
                            self.total_views = "Не удалось получить просмотры за все время"
                        try:
                            self.today_views = self.driver.find_element(
                                By.CSS_SELECTOR, '[data-marker="item-view/today-views"]').text
                        except:
                            self.today_views = "Не удалось получить просмотры за сегодня"
                        try:
                            type = self.driver.find_element(

                                By.CSS_SELECTOR, '[data-marker="seller-info/label"]').text
                        except:
                            type = "Компания"
                        try:
                            self.category = self.driver.find_elements(
                                By.CLASS_NAME, "breadcrumbs-linkWrapper-jZP0j")[2].text
                        except:
                            self.category = "Не удалось получить категорию товара"

                        try:
                            # self.time = datetime.now()
                            self.time = self.time.strftime(
                                "%m/%d/%Y, %H:%M:%S")
                        except:
                            self.time = "Ошибка"

                        try:
                            self.button = self.driver.find_element(
                                By.CSS_SELECTOR, '[data-marker="item-phone-button/card"]')
                            self.button.click()
                            sleep(10)
                            try:
                                self.data1 = self.driver.find_element(
                                    By.CLASS_NAME, "item-popup-phoneImage-adVhz").get_attribute("src")
                                self.data1 = self.data1.split(
                                    'data:image/png;base64,')[1]
                                self.img_data = b64decode(self.data1)
                                with open("img.png", "wb") as file:
                                    file.write(self.img_data)
                                self.image = Image.open("img.png")
                                self.phone_number = pytesseract.image_to_string(
                                    self.image)
                            except:
                                self.phone1 = self.driver.find_element(
                                    By.CLASS_NAME, "contacts-call-button-exp-phone__button-_bJym")
                                self.phone1.click()
                                sleep(1)
                                self.data1 = self.driver.find_element(
                                    By.CLASS_NAME, "contacts-call-button-exp-phone-s2PKx").get_attribute("src")
                                self.data1 = self.data1.split(
                                    'data:image/png;base64,')[1]
                                self.img_data = b64decode(self.data1)
                                with open("img.png", "wb") as file:
                                    file.write(self.img_data)
                                self.image = Image.open("img.png")
                                self.phone_number = pytesseract.image_to_string(
                                    self.image)

                        except Exception as ex:
                            print(ex)
                            self.phone_number = "Не удалось определить номер телефона"
                        try:
                            self.close_button = self.driver.find_element(
                                By.CLASS_NAME, 'popup-close-XlIOw')
                            self.close_button.click()
                            sleep(2)  # 2
                            self.user1 = self.driver.find_element(
                                By.CLASS_NAME, "style-seller-name-link-_yAhr")
                            self.user1.click()
                            sleep(1)  # 2
                            self.user_url_demo = self.driver.current_url
                            self.user_url = self.user_url_demo.split(
                                "?")[0].replace("?", "")
                            # if type == "Частное лицо":
                            try:
                                self.orders_points = self.driver.find_element(
                                    By.CLASS_NAME, "Tabs-nav-tab-title-OGjV6").text
                            # else:
                            except:
                                self.orders_points = self.driver.find_elements(
                                    By.CLASS_NAME, "desktop-1r4tu1s")[1].text
                        except Exception as ex:
                            print(ex)
                            self.user_url = "Не удалось получить ссылку на пользователя"
                            self.orders_points = "Не удалось получить количество активных объявлений пользователя"
                        try:
                            self.now_time = time.strftime("%m/%d/%Y, %H:%M:%S")
                        except:
                            self.now_time = "Ошибка"

                        self.result_list.append(self.title)
                        self.result_list.append(self.url)
                        self.result_list.append(self.price)
                        self.result_list.append(self.username)
                        self.result_list.append(self.location)
                        self.result_list.append(self.score)
                        self.result_list.append(self.reviews)
                        self.result_list.append(self.category)
                        self.result_list.append(self.describe)
                        self.result_list.append(self.total_views)
                        self.result_list.append(self.today_views)
                        self.result_list.append(type)
                        self.result_list.append(self.phone_number)
                        self.result_list.append(self.now_time)
                        self.result_list.append(self.piar_uslugi)
                        self.result_list.append(self.user_url)
                        self.result_list.append(self.orders_points)
                        self.array = {"values": self.list1}
                        self.response = self.service.append(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                                                            range=self.range_, valueInputOption="USER_ENTERED", body=self.array).execute()
                        self.result_list.clear()

                        sleep(5)  # 10
                        self.driver.close()
                        self.driver.switch_to.window(
                            self.driver.window_handles[0])
                    try:
                        self.button_next = self.driver.find_elements(
                            By.CLASS_NAME, 'pagination-item_arrow-Sttbt')[1]
                        self.button_next.click()
                    except:
                        print("Страницы с объявлениями закончились")

            except Exception as ex:
                print(ex)
            finally:
                # driver.close()
                # driver.quit()
                pass

    def call_analyze(self):
        self.range_ = "Sheet2!A1:Z1000"
        # self.url = "https://www.avito.ru/ufa/avtomobili?cd=1&radius=200"
        self.url = self.dictionary[self.category]

        try:
            self.driver.get(url=self.url)
            # login_button = driver.find_element(
            # By.CSS_SELECTOR, "[data-marker='header/login-button']")
            # login_button.click()
            # driver.implicitly_wait(10)
            # log_button = driver.find_element(
            # By.CSS_SELECTOR, "[data-marker='login-form/login']")
            # log_button.send_keys("79061071451")
            # password_button = driver.find_element(
            # By.CSS_SELECTOR, "[data-marker='login-form/password']")
            # password_button.send_keys("16031984@Dd")
            # confirm_button = driver.find_element(
            # By.CSS_SELECTOR, '[data-marker="login-form/submit"]')
            # confirm_button.click()
            # time.sleep(60)

            #self.city = "Новосибирск"

            try:
                self.location_form = self.driver.find_element(
                    By.CSS_SELECTOR, '[data-marker="search-form/region"]')
                self.location_form.click()
                sleep(2)
                self.location_input = self.driver.find_element(
                    By.CLASS_NAME, "suggest-input-rORJM")
                self.location_input.click()
                self.location_input.send_keys(self.city)
                sleep(5)
                try:
                    self.first_reuslt = self.driver.find_element(
                        By.CSS_SELECTOR, '[data-marker="suggest(0)"]')
                    self.first_reuslt.click()
                except:
                    print("Не правильный поиск локации")
                finally:
                    sleep(5)
                    self.confirm = self.driver.find_element(
                        By.CSS_SELECTOR, '[data-marker="popup-location/save-button"]')

                    self.confirm.click()
            except Exception as ex:
                print(ex)
            for self.x in range(1, ((int(self.pages)+1))):
                self.ads = self.driver.find_elements(
                    By.CLASS_NAME, 'iva-item-root-_lk9K')
                self.piar_list = {}
                for self.ad in self.ads:
                    if self.checkPiar:
                        try:
                            self.arrow = self.ad.find_element(
                                By.CLASS_NAME, "styles-arrow-jfRdd")
                            self.hover = ActionChains(self.driver).move_to_element(
                                self.arrow).perform()
                            sleep(2)
                            self.piar_data = self.driver.find_elements(
                                By.CLASS_NAME, "styles-entry-MuP_G")

                            self.piar_list.clear
                            for self.piar in self.piar_data:
                                self.piar_text = self.piar.find_element(
                                    By.CLASS_NAME, "styles-title-nWv6g").text
                                self.piar_image = self.piar.find_element(
                                    By.CLASS_NAME, "style-image-wPviB").get_attribute("src")
                                self.spliter = self.piar_image.split(
                                    "https://www.avito.st/s/common/components/monetization/icons/web/")[1]
                                self.piar_orders = self.spliter.replace(
                                    ".svg", "")
                                if len(self.piar_data) == 0:
                                    self.piar_list = "Не использовано услуг продвижения"
                                else:
                                    if "_1" in self.piar_orders:

                                        self.piar_list[self.piar_text] = self.piar_orders
                                    else:
                                        self.piar_list[self.piar_text] = "True"
                                    self.strings = []
                                for self.key, self.item in self.piar_list.items():
                                    self.strings.append("{}: {}".format(
                                        self.key.capitalize(), self.item))
                                self.piar_uslugi = "; ".join(self.strings)
                                self.strings.clear()
                        except Exception as ex:
                            print(ex)
                            self.piar_uslugi = "Не использовано услуг продвижения"
                        sleep(2)

                    else:
                        self.piar_uslugi = "-"
                    sleep(1)
                    self.ads2 = self.ad.find_element(
                        By.CLASS_NAME, "iva-item-title-py3i_")
                    self.ads2.click()

                    self.driver.implicitly_wait(5)
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    sleep(2)

                    try:
                        self.title = self.driver.find_element(
                            By.XPATH, "//span[@data-marker='item-view/title-info']").text
                    except:
                        self.title = "Не удалось получить название объявления"

                    self.url = self.driver.current_url
                    try:
                        self.price = self.driver.find_element(
                            By.CLASS_NAME, "style-item-price-text-_w822").text
                    except:
                        self.price = "Не удалось определить цену"

                    try:
                        self.username = self.driver.find_element(
                            By.XPATH, "//div[@data-marker='seller-info/name']").text
                    except:
                        self.username = "Не удалось определить имя пользователя"

                    try:
                        self.location = self.driver.find_element(
                            By.CLASS_NAME, "style-item-address__string-wt61A").text
                    except:
                        self.location = "Не получилось определить адресс"

                    try:
                        self.score = self.driver.find_element(
                            By.CLASS_NAME, "style-seller-info-rating-score-C0y96").text
                    except:
                        self.score = "У пользователя нет рейтинга"

                    try:
                        self.reviews = self.driver.find_element(
                            By.XPATH, "//span[@data-marker='rating-caption/rating']").text
                    except:
                        self.reviews = "У пользователя нет отзывов"
                    try:
                        self.describe = self.driver.find_element(
                            By.XPATH, "//div[@data-marker='item-view/item-description']").text
                    except:
                        self.describe = "Не удалось получить описание товара"
                    try:
                        self.since = self.driver.find_elements(
                            By.CLASS_NAME, "style-seller-info-value-vOioL")[1].text
                    except:
                        self.since = "Не удалось определить с какого времени продавец на авито"

                    if self.checkAllViews:
                        try:
                            self.total_views = self.driver.find_element(
                                By.CSS_SELECTOR, '[data-marker="item-view/total-views"]').text
                        except Exception as _ex:
                            print(_ex)
                            self.total_views = "Не удалось получить просмотры за все время"
                    else:
                        self.total_views = "-"

                    if self.checkDayViews:
                        try:
                            self.today_views = self.driver.find_element(
                                By.CSS_SELECTOR, '[data-marker="item-view/today-views"]').text
                        except:
                            self.today_views = "Не удалось получить просмотры за сегодня"
                    else:
                        self.today_views = "-"

                    try:
                        type = self.driver.find_element(
                            By.CSS_SELECTOR, '[data-marker="seller-info/label"]').text
                    except:
                        type = "Компания"

                    try:
                        self.category = self.driver.find_elements(
                            By.CLASS_NAME, "breadcrumbs-linkWrapper-jZP0j")[2].text
                    except:
                        self.category = "Не удалось получить категорию товара"

                    try:
                        self.time = datetime.now()
                    except:
                        self.time = "Ошибка"

                    if self.checkPhone:
                        try:
                            self.button = self.driver.find_element(
                                By.CSS_SELECTOR, '[data-marker="item-phone-button/card"]')
                            self.button.click()
                            sleep(10)
                            try:
                                self.data1 = self.driver.find_element(
                                    By.CLASS_NAME, "item-popup-phoneImage-adVhz").get_attribute("src")
                                self.data1 = self.data1.split(
                                    'data:image/png;base64,')[1]
                                self.img_data = b64decode(self.data1)
                                with open("img.png", "wb") as file:
                                    file.write(self.img_data)
                                self.image = Image.open("img.png")
                                self.phone_number = pytesseract.image_to_string(
                                    self.image)
                            except:
                                sleep(5)
                                self.phone1 = self.driver.find_element(
                                    By.CSS_SELECTOR, "[data-marker='show-phone']")
                                self.phone1.click()
                                sleep(3)
                                self.data1 = self.driver.find_element(
                                    By.CSS_SELECTOR, "[data-marker='phone-popup/phone-image']").get_attribute("src")
                                self.data1 = self.data1.split(
                                    'data:image/png;base64,')[1]
                                self.img_data = b64decode(self.data1)
                                with open("img.png", "wb") as file:
                                    file.write(self.img_data)
                                self.image = Image.open("img.png")
                                self.phone_number = pytesseract.image_to_string(
                                    self.image)

                        except Exception as ex:
                            print(ex)
                            self.phone_number = "Не удалось определить номер телефона"
                    else:
                        self.phone_number = "-"

                    try:
                        self.close_button = self.driver.find_element(
                            By.CLASS_NAME, 'popup-close-XlIOw')
                        self.close_button.click()
                        sleep(2)
                        self.user1 = self.driver.find_element(
                            By.CLASS_NAME, "style-seller-name-link-_yAhr")
                        self.user1.click()
                        sleep(2)
                        self.user_url_demo = self.driver.current_url
                        self.user_url = self.user_url_demo.split(
                            "?")[0].replace("?", "")
                        # if type == "Частное лицо":
                        try:
                            self.orders_points = self.driver.find_element(
                                By.CLASS_NAME, "Tabs-nav-tab-title-OGjV6").text
                        # else:
                        except:
                            self.orders_points = self.driver.find_elements(
                                By.CLASS_NAME, "desktop-1r4tu1s")[1].text
                    except Exception as ex:
                        print(ex)
                        self.user_url = "Не удалось получить ссылку на пользователя"
                        self.orders_points = "Не удалось получить количество активных объявлений пользователя"
                    try:
                        self.now_time = self.time.strftime(
                            "%m/%d/%Y, %H:%M:%S")
                    except:
                        self.now_time = "Ошибка"

                    self.response = self.service.get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                                                     range=self.range_).execute()
                    # if self.user_url not in self.response:
                    # if (self.score not in self.response) and (self.reviews not in self.response) and (self.orders_points not in self.response):
                    self.result_list.append(self.title)
                    self.result_list.append(self.url)
                    self.result_list.append(self.price)
                    self.result_list.append(self.username)
                    self.result_list.append(self.location)
                    self.result_list.append(self.score)
                    self.result_list.append(self.reviews)
                    self.result_list.append(self.category)
                    self.result_list.append(self.describe)
                    self.result_list.append(self.total_views)
                    self.result_list.append(self.today_views)
                    self.result_list.append(type)
                    self.result_list.append(self.phone_number)
                    self.result_list.append(self.now_time)
                    self.result_list.append(self.piar_uslugi)
                    self.result_list.append(self.user_url)
                    self.result_list.append(self.orders_points)
                    if self.result_list not in self.response:
                        self.array = {"values": self.list1}
                        self.response = self.service.append(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                                                            range=self.range_, valueInputOption="USER_ENTERED", body=self.array).execute()
                    self.result_list.clear()

                    sleep(10)
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                try:
                    self.button_next = self.driver.find_elements(
                        By.CLASS_NAME, 'pagination-item_arrow-Sttbt')[1]
                    self.button_next.click()
                except:
                    print("Страницы с объявлениями закончились")
        except Exception as ex:
            print(ex)
        finally:
            # driver.close()
            # driver.quit()
            pass

# scapper=Scrap()
# scapper.search()
# print(datetime.now())
