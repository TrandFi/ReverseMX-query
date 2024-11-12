import dns.resolver #  Библиотека для работы с DNS
from prettytable import PrettyTable #  Библиотека для работы с таблицами

input_domain = input("Введите домен \n >")
print("\nMX Records for domain:",input_domain)
try:
    mxrecords_list = dns.resolver.resolve(input_domain, "MX") #  Для переданного домена находим все MX-записи
    mx_table = PrettyTable(["MX record","Priority"]) #  Создаем таблицу и описываем заголовки столбцов
    for record in mxrecords_list:
        output = record.to_text().split() #  Разделяем MX-запись для удобного вывода в таблице            
        mx_table.add_row([output[1], output[0]]) #  Выводим запись в виде [ № приоритета, MX-запись ]
    print(mx_table)
except Exception: #  В случае, если домен не содержит MX-записи или он введен неверно
    print("MX Records do not exist")