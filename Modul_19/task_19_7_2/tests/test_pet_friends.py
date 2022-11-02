from api import PetFriends
from settings import valid_email, valid_password, valid_email1, valid_password1, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
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


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#Далее начинаются мои тесты

#1
def test_add_new_pet_without_photo_with_valid_data(name='Пушок', animal_type='британец', age='2'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
#2
def test_add_photo_of_pet_with_valid_data(pet_photo='images/cat.jpg'):
    """Проверяем возможность добавления фото питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Флаг наличия животного без фото
    flag = False

    # Перебираем список и ищем питомца без фото
    for key in range(0, len(my_pets['pets'])):
        if my_pets['pets'][key]['pet_photo'] == '':
            # Если питомец без фото нашелся, то меняем значение флага
            flag = True
            # Добавляем фото
            status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][key]['id'], pet_photo)
            # Сверяем полученный ответ с ожидаемым результатом
            assert status == 200
            assert result['pet_photo'] != ''
            # Выходим из цикла
            break
    # Если в сипске питомцев нет животных без фото, то выдаем об этом сообщение
    if flag == False:
        raise Exception("Нет животных без фото")
#3
def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем что при вводе неверного пароля пользователь не может получить API key"""
    status, result = pf.get_api_key(email, password)

    # Проверяем что статус ответа равен 403 и в ответе нет ключа
    assert status == 403
    assert 'key' not in result
#4
def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """Проверяем что при вводе неверного email пользователь не может получить API key"""
    status, result = pf.get_api_key(email, password)

    # Проверяем что статус ответа равен 403 и в ответе нет ключа
    assert status == 403
    assert 'key' not in result
#5
def test_add_new_pet_with_text_age(name='Барбоскин', animal_type='двортерьер', age='homeless'):
    """Проверяем невозможность создания питомца, возраст которого не является числом
    Тест не проходит, т.к. значение поля возраст не контролируется"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
#6
def test_add_new_pet_with_incorrect_age(name='Барбоскин', animal_type='двортерьер', age='-57'):
    """Проверяем невозможность создания питомца, возраст которого меньше 0>
    Тест не проходит, т.к. значение поля возраст не контролируется"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
#7
def test_add_new_pet_without_data(name='', animal_type='', age=''):
    """Проверяем, что нельзя добавить питомца не указывая никакие данные
    Тест не проходит, т.к. заполнение полей не контролируется"""


    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
#8
def test_unsuccessful_update_self_pet_info_with_incorrect_age(name='Пух', animal_type='Медведь', age='Трям'):
    """Проверяем невозможность обновления информации о питомце,
    в случае указания нового возраста не являющегося целым числом
    Тест не проходит, т.к. значение поля возраст не контролируется"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 400
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#9
def test_unsuccessful_delete_other_pet():
    """Проверяем невозможность удаления чужого питомца
    Тест не проходит, т.к. любой авторизованный пользователь может удалить чужого питомца"""

    # Получаем ключи auth_key двух пользователей
    _, auth_key_user1 = pf.get_api_key(valid_email, valid_password)
    _, auth_key_user2 = pf.get_api_key(valid_email1, valid_password1)

    #запрашиваем список своих питомцев пользователя User1
    _, my_pets = pf.get_list_of_pets(auth_key_user1, "my_pets")

    # Проверяем - если список своих питомцев user1 пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key_user1, "Суперкот", "кот", "3", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key_user1, "my_pets")

    # Берём id первого питомца из списка User1 и отправляем запрос на удаление с API key User2
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key_user2, pet_id)

    # Ещё раз запрашиваем список своих питомцев User1
    _, my_pets = pf.get_list_of_pets(auth_key_user1, "my_pets")

    # Проверяем что статус ответа равен 403 и в списке питомцев остался питомец, которого мы пытались удалить
    assert status == 403
    assert pet_id in my_pets.values()

#10
def test_unsuccessful_update_other_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем невозможность обновления информации о чужом питомце
    Тест не проходит, т.к. любой авторизованный пользователь может обновить информацию о чужом питомце"""

    # Получаем ключи auth_key двух пользователей
    _, auth_key_user1 = pf.get_api_key(valid_email, valid_password)
    _, auth_key_user2 = pf.get_api_key(valid_email1, valid_password1)

    # запрашиваем список своих питомцев пользователя User1
    _, my_pets = pf.get_list_of_pets(auth_key_user1, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст с API key другого пользователя
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key_user2, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 403
        assert status == 403
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")