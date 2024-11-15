# Программа, которая реализует ReverseMX запрос

## Инструменты
Программа написана на языке программирования python3

## Документация
В программе используются для библиотеки:
1. ipaddress - Обработка IP адресов
2. socket - Работа с серверами
3. requests - Работа с HTTP-запросами к веб-страницам
4. prettytable - Работа с таблицами

## Установка
Все библиотеки подгружены в файл виртуальной среды requirements.txt, который автоматически загружает указанные библиотеки при запуске программы

## Основная логика получения MX-запросов по шагам

1. Ввод пользователем имени доменного сервера
```python
domain = input("Input domain server name for search:\n>")
```
2. Получение IP-адреса указанного домена с помощью функции ip_lookup(domain_name)
```python
def ip_lookup(domain_name):
    try:
        ip = socket.gethostbyname(domain_name)  #  Возвращает имя хоста (домен сервера) по заданному ip-адресу
        return ip
    except:
        return None

ip_domain = ip_lookup(domain)
```
3. Составление запроса на веб-сайт ViewDNS с указанием IP-адреса нужного нам хоста и нашего API ключа
```python
url = f"https://api.viewdns.info/reverseip/?host={ip}&apikey={API_KEY_FROM_VIEWDNS}&output=json" #  Формируем запрос на сайт ViewDNS, указывая IP нудного нам хоста и наш API ключ
```
4. Отправка запроса на сайт и получение данных в виде словаря, используя функцию json()
```python
response = requests.get(url)  #  Отправляем запрос на указанный ресурс
if response.ok:  #  В случае положительного соединения с хостом
   data = response.json()  #  Преобразуем ответ в json формат
   #  Данная функция автоматически преобразует объект ответа от хоста в словарь
```
5. Выборка необходимых данных по ключам словаря data
```python
if "response" in data and "domains" in data["response"]:  #  Проверяем наличие ключей "response" и "domains" в словаре data
      domainlist = data["response"]["domains"]  #  Записываем в переменную значение ключа response[domains]. 
      #  В результате переменная websites будет иметь тип списка list, каждым элементом которого является словарь dictionaty
```
6. Вывод полученных данных в виде таблицы
```python
if domainlist != []:
   print(len(domainlist),"subdomains were found on this server:")         
   for d in domainlist:
       i+=1  
       table.add_row([i, d["name"], d["last_resolved"]])                                                       
   print(table)
else:
   print("[-] No other websites found on the same server.")   
```
