import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(autouse=True)
def testing():
    # Автоматически загружаем Гугл-драйвер (предварительно установили pip install webdriver-manager)
    pytest.driver = webdriver.Chrome(ChromeDriverManager().install())
    # pytest.driver = webdriver.Chrome('/GoogleDriver/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    time.sleep(5)

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('lelya10.92@mail.ru')
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    # Вводим пароьл
    pytest.driver.find_element(By.ID, 'pass').send_keys('2210la')
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
    # Нажимаем на кнопку входа в аккаунт
    WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку "Мои питомцы"
    pytest.driver.find_element(By.CSS_SELECTOR, 'div#navbarNav > ul > li > a').click()
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))

    # 1. Написать тест, который проверяет, что присутствуют все питомцы

    # Считаем кол-во строк в таблице:
    row_count = len(pytest.driver.find_elements(By.TAG_NAME, 'tr'))
    # Читаем данные о количестве питомцев слева от таблицы:
    my_pet_amount = pytest.driver.find_element(By.XPATH, '(html/body/div[1]/div[1]/div[1])')
    my_pet_amount = my_pet_amount.get_attribute('innerText')
    # Сравниваем:
    assert str((row_count) - 1) in my_pet_amount

    # 2. Написать тест, который проверяет, что хотя бы у половины питомцев есть фото.
    # Включаем счётчик фото:
    kol_vo_photo = 0
    # Получаем список моих питомцев с фото:
    photos = pytest.driver.find_elements(By.XPATH, "//tbody/tr/th/img")
    # Считаем кол-во:
    for i in range(len(photos)):
        if 'data' in photos[1].get_attribute('src'):
            kol_vo_photo += 1
    # Сравниваем кол-во фото с числом, равным половине моих питомцев:
    assert kol_vo_photo >= (row_count - 1) / 2


# 3. У всех питомцев есть имя, возраст и порода.

    names = pytest.driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
    breed = pytest.driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
    age = pytest.driver.find_elements(By.XPATH, "//tbody/tr/td[3]")

    for i in range(len(names)):
        assert names[i].text != ''
        assert breed[i].text != ''
        assert age[i].text != ''

# 4. У всех питомцев разные имена.
    for i in range(len(names)):
        assert names[i].text != names[i-1].text

# 5. В списке нет повторяющихся питомцев.




