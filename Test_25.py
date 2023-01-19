import pytest, itertools
from settings import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.engine = webdriver.Chrome('chromedriver.exe')
    pytest.engine.fullscreen_window()
    pytest.engine.maximize_window()
    pytest.engine.implicitly_wait(10)
    pytest.engine.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.engine.find_element(By.ID, "email").send_keys(valid_email)
    # Вводим пароль
    pytest.engine.find_element(By.ID, "pass").send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.engine.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    yield
    pytest.engine.quit()

def test_show_my_pets():
    # Переходим на вкладку Мои питомцы
    pytest.engine.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Проверяем Вход в учетную запись с определенным Никнеймом
#    assert pytest.engine.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/h2').text == "Viktor Tyamin"

def test_my_pets_variables():
    pet_number_photo, i, j, mass_of_pet_data, mass_of_pet_names = 0, 1, 1, [], []
    # Переходим на вкладку Мои питомцы
    pytest.engine.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Находим количество питомцев в тексте
    general_text = pytest.engine.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text
    pet_number_in_text = int(general_text.split("\n")[1].split(' ')[1])
    # Находим действительное количество питомцев на странице пользователя
    pet_number_real = len(pytest.engine.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr'))
    # Ожидаем появления таблицы питомцев на странице
    table = WebDriverWait(pytest.engine, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="all_my_pets"]/table')))
    # Находим:
    for i in range(1, pet_number_real + 1):
        pet_data = []
    # количество фотографий питомцев и питомца, не имеющего фотографии
        photo_of_pet = pytest.engine.find_element(By.XPATH, f'//*[@id="all_my_pets"]/table/tbody/tr[{i}]/th/img').size
        if photo_of_pet != {'height': 0, 'width': 0}:
            pet_number_photo = pet_number_photo + 1
        else:
            print(f'\nA pet number {i} has no a photo')
    # все данные питомца, исключая фотографии, и вычленяем из них список имен питомцев
        for j in range (1, 4):
            text = pytest.engine.find_element(By.XPATH, f'//*[@id="all_my_pets"]/table/tbody/tr[{i}]/td[{j}]').text
            pet_data.append(text)
        mass_of_pet_data.append(pet_data)
        mass_of_pet_names.append(mass_of_pet_data[i-1][0])
    # Ожидания
    assert pet_number_in_text == pet_number_real
    assert pet_number_photo >= pet_number_real / 2
    for i, j in itertools.product(range(0, pet_number_real), range(0, 3)):
        try:
            assert mass_of_pet_data[i][j] != ""
        except AssertionError:
            print(f"\nA pet number {i + 1} has no attribute {j + 1}")
    assert sorted(mass_of_pet_names) == sorted(set(mass_of_pet_names))
