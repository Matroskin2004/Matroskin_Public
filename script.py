per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}
money = float(input('Сумма вклада в рублях:\n')) #Получаем от пользователя сумму вкалада
deposit = list(per_cent.values())
deposit = [int(i * money / 100) for i in deposit]
print('Максимальная сумма, которую вы можете заработать ' + str(max(deposit)) + ' рублей')

