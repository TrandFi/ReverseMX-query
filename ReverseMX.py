import ipaddress #  Обработка IP адресов
import socket #  Работа с серверами
import requests  # Работа с HTTP-запросами к веб-страницам
from prettytable import PrettyTable #  Библиотека для работы с таблицами

API_KEY_FROM_VIEWDNS = "13e89d74db1aa14da7246b65b2fc110ecf60a8a0" #  API ключ с сайта ViewDNS

def is_valid_ip(ip): #  Функция провери корректности (существования) IP адреса
    try:
        ipaddress.ip_address(ip) #  Проверка IP-адреса. 
        #Если адрес не является допустимым адресом IPv4, то возникает ошибка AddressValueError (поскольку дання функция возвращает тип IPv4)

        return True
    except ValueError:
        return False


def ip_lookup(domain_name):
    try:
        ip = socket.gethostbyname(domain_name)  #  Возвращает имя хоста (домен сервера) по заданному ip-адресу
        return ip
    except:
        return None


def get_domains_from_viewdns(ip):
    url = f"https://api.viewdns.info/reverseip/?host={ip}&apikey={API_KEY_FROM_VIEWDNS}&output=json" #  Формируем запрос на сайт ViewDNS, указывая IP нудного нам хоста и наш API ключ
    response = requests.get(url)  #  Отправляем запрос на указанный ресурс
    if response.ok:  #  В случае положительного соединения с хостом
        data = response.json()  #  Преобразуем ответ в json формат
        #  Данная функция автоматически преобразует объект ответа от хоста в словарь

        if "response" in data and "domains" in data["response"]:  #  Проверяем наличие ключей "response" и "domains" в словаре data
            domainlist = data["response"]["domains"]  #  Записываем в переменную значение ключа response[domains]. 
            #  В результате переменная websites будет иметь тип списка list, каждым элементом которого является словарь dictionaty
            
            return domainlist
    return [] #  Возвращаем пустой список, если по указанному домену сервера не было найдено поддоменов

def main():
    table = PrettyTable(["№","Domain name","Last resolved"])
    i = 0
    domain = input("Input domain server name for search:\n>")
    ip_domain = ip_lookup(domain)
    if not is_valid_ip(ip_domain):
        print(f"\n[error] Invalid IP address for: {domain}")     
    else:
        print(f"\n[success] Domain server: {domain}, IP: {ip_domain}\n")
        domainlist = get_domains_from_viewdns(ip_domain)
        if domainlist != []:
            print(len(domainlist),"subdomains were found on this server:")         
            for d in domainlist:
                i+=1  
                table.add_row([i, d["name"], d["last_resolved"]])                                                       
            print(table)
        else:
            print("[-] No other websites found on the same server.")   
main()
