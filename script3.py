import PySimpleGUI as sg
import os
import requests
from bs4 import BeautifulSoup
import datetime

def read_urls_from_file(filename):
    with open(filename, 'r') as file:
        urls = [line.strip() for line in file]
    return urls

def check_product_availability(urls):
    for url in urls:
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        item_flag = soup.find('li', class_='item-flag')
        if item_flag is not None:
            available_text = item_flag.find('span').text
            if available_text == "Novedad":
                next_sibling = item_flag.find_next_sibling('li', class_='item-flag')
                if next_sibling is not None:
                    available_text = next_sibling.find('span').text
            print(f'{url} - {available_text}\n')
        else:
            print(f'{url} - No se encontró el elemento <li> con la clase "item-flag"')

layout = [
    [sg.Text('Selecciona el archivo de texto que contiene las URLs a comprobar:')],
    [sg.Input(), sg.FileBrowse()],
    [sg.Button('Comprobar'), sg.Button('Cancelar')]
]

window = sg.Window('Comprobador de disponibilidad de productos', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar':
        break
    elif event == 'Comprobar':
        filename = values[0]
        urls = read_urls_from_file(filename)

        load_window = sg.popup('Cargando...', auto_close=True, auto_close_duration=2)

        check_product_availability(urls)

        today = datetime.datetime.today().strftime('%Y-%m-%d')
        filename = f'check_{today}.txt'

        with open(filename, 'w') as file:
            for url in urls:
                response = requests.get(url)
                html = response.content
                soup = BeautifulSoup(html, 'html.parser')
                item_flag = soup.find('li', class_='item-flag')
                if item_flag is not None:
                    available_text = item_flag.find('span').text
                    if available_text == "Novedad":
                        next_sibling = item_flag.find_next_sibling('li', class_='item-flag')
                        if next_sibling is not None:
                            available_text = next_sibling.find('span').text
                    if available_text != "Disponible":
                        file.write(f'{url} - {available_text}\n')
                else:
                    file.write(f'{url} - No se encontró el elemento <li> con la clase "item-flag"\n')

        sg.popup('La comprobación ha finalizado.\n\nLos resultados se han guardado en el archivo "{}".'.format(filename), title='Comprobación finalizada')

window.close()
