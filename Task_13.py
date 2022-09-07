sum=int(0)                                                                              # Общая стоиомсть билетов участников
try:
    number = int(input('Введите колличество билетов:\n'))                               # колличество билетов
except ValueError as number:                                                            # проверяем корректность ввода
    print('Колличество билетов должно быть целым числом')                               # выводим сообщение, если введено не целое число
else:
    if number<1:                                                                        # проверяем корректность ввода
        print ('Колличесво билетов не может быть меньше 1')                             # выводим сообщение, если количество меньше 1
    else:
        if number>3:                                                                    # проверяем возможность предоставления скидки
            discount=0.9                                                                # применяем скидку
        else:
            discount=1                                                                  # не применяем скидку
        for i in range(number):
            try:
                print('Введите возраст участника ',i+1)                                 # запрашиваем возраст участников
                age = int(input())
            except ValueError as age:                                                   # проверяем корректность ввода
                print('Возраст участника должен быть целым числом')                     # выводим сообщение, если введено не целое число
                break
            else:
                if age < 0 or age > 100:                                                # проверяем корректность ввода
                    print('Возраст участника не может быть меньше 0 и больше 100 лет')  # выводим сообщени, если возраст вне допустимого диапозона
                    break
                else:
                    if age < 18:                                                        # если возраст участника меньше 18 лет, то сумма не меняется
                        sum+=0
                    if 18 <= age < 25:                                                  # если возраст участника от 18 до 25, то сумма увеличивается на 990, дисконт учитывается
                        sum+=990*discount
                    if age >= 25:                                                       # если возраст участника 25 лет или более, то сумма увеличивается на 1390, дисконт учитывается
                        sum+=1390*discount
        if i+1 == number:                                                               # если данные всех участников были введены корректно, то выводим общую стоиость билетов
            print('Общая стоимость билетов:',sum,'руб.')