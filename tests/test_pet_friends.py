from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os
import pytest

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """Проверяем, что запрос api ключа возвращает статус 403 """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key_invalid(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем, что запрос api ключа возвращает статус 403 """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key_invalid(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверяем, что запрос api ключа возвращает статус 403 """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key_invalid(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список. Для этого сначала
    получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ, запрашиваем
    список всех питомцев и проверяем, что список не пустой. Доступное значение параметра
    filter - 'my_pets' либо ''"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Багира', animal_type='пантера',
                                     age='4', pet_photo='images/cat.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_simple_with_valid_data(name='Бобик', animal_type='пёс', age='2'):
    """Проверяем, что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_pet_photo(pet_photo='images/bobik.jpg'):
    """Проверяем возможность добавления фото питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
        assert status == 200
        assert result['pet_photo'] == pet_photo


def test_add_pet_video(pet_photo='images/koshak.mp4'):
    """Проверяем невозможность добавления видео питомца вместо фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
        assert status == 500

def test_add_pet_invalid_photo(name='Бобик', animal_type='пёс', age='2', pet_photo='images/nonexistent.jpg'):
    """Проверяем, что неверный путь к файлу или несуществующий файл вызывают исключение"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        # Добавляем питомца с неверным путем к файлу или несуществующим файлом
        status, result = pf.add_pet_photo(auth_key, name, animal_type, age, pet_photo)
    except FileNotFoundError:
        # Проверяем, что исключение FileNotFoundError было вызвано
        assert True
    else:
        # Если исключение не было вызвано, то тест не прошел
        assert False

def test_add_new_pet_without_name(animal_type='кролик', age='1'):
    """Проверяем, что невозможно добавить питомца без обязательного поля 'name'"""

    #Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name=None, animal_type=animal_type, age=age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

def test_add_new_pet_without_animal_type(name='Барсик', age='1'):
    """Проверяем, что невозможно добавить питомца без обязательного поля 'animal_type'"""

    #Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name=name, animal_type=None, age=age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

def test_add_new_pet_without_age(name='Пушок', animal_type='кролик'):
    """Проверяем, что невозможно добавить питомца без обязательного поля 'age'"""

    #Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name=name, animal_type=animal_type, age=None)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
