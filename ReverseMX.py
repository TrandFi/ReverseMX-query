import ipaddress
import socket
import requests  # работа с HTTP-запросами к веб-страницам
from prettytable import PrettyTable #  Библиотека для работы с таблицами

API_KEY_FROM_VIEWDNS = "13e89d74db1aa14da7246b65b2fc110ecf60a8a0"

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def ip_lookup(domain_name):
    try:
        ip = socket.gethostbyname(domain_name)  #  Возвращает имя хоста (домен сервера) по заданному ip-адресу
        return ip
    except:
        return None


def get_websites_on_server(ip):
    url = f"https://api.viewdns.info/reverseip/?host={ip}&apikey={API_KEY_FROM_VIEWDNS}&output=json"
    response = requests.get(url)  #  Отправляем запрос на указанный ресурс
    if response.ok:  #  В случае положительного соединения с хостом
        data = response.json()  #  Преобразуем ответ в json формат
        #  Данная функция автоматически преобразует объект ответа от хоста в словарь

        if "response" in data and "domains" in data["response"]:  #  Проверяем наличие ключей "response" и "domains" в словаре ответа хоста
            websites = data["response"]["domains"]  #  Записываем в переменную значение ключа response[domains]. 
            #  В результате переменная websites будет иметь тип списка list, каждым элементом которого является словарь dictionaty
            
            return websites
    return [] #  Возвращаем пустой список, если по указанному домену сервера не было найдено поддоменов

def main():
    table = PrettyTable(["№","Domain name","Last resolved"])
    i = 0
    domain = input()
    ip_domain = ip_lookup(domain)
    if not is_valid_ip(ip_domain):
        print(f"\n[error] Invalid IP address for: {domain}")     
    else:
        print(f"\n[success] Domain server: {domain}, IP: {ip_domain}\n")
        websites = get_websites_on_server(ip_domain)
        if websites != []:
            print(len(websites),"subdomains were found on this server:")         
            for website in websites:
                i+=1  
                table.add_row([i, website["name"], website["last_resolved"]])                                         
                #print(f"[+] {website["last_resolved"]}")
            print(table)
        else:
            print("[-] No other websites found on the same server.")   
main()
