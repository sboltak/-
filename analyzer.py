import pandas as pd
import matplotlib.pyplot as plt
import requests
import time

host = 'https://boltak.lab402.by'
group_id = 'bsuir_official'


def createPieChart(labels, sizes, name): #создание круговой диаграммы
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.5f%%')
    plt.legend(loc='best')

    image_format = 'svg'
    image_name = name + '.svg'
    plt.savefig(image_name, format=image_format, dpi=1200, bbox_inches="tight")  # save the figure to file
    plt.close(fig)

def createBarChart(data, name): #создание гистограммы
    fig, ax = plt.subplots()
    plt.legend(loc='best')

    #ds.plot.bar(rot=0)
    names = list(data.keys())
    values = list(data.values())

    plt.bar(range(len(data)), values, tick_label=names)
    image_format = 'svg'
    image_name = name + '.svg'
    plt.savefig(image_name, format=image_format, dpi=1200, bbox_inches="tight")  # save the figure to file
    plt.close(fig)


response = requests.get(
        '{host}/sex/{group_id}'
        .format(host=host, group_id=group_id))

response = response.json()

#создание круговой диаграммы по полу
labels = response['labels']
sizes = response['sizes']

createPieChart(labels, sizes, 'closed')

#создание круговой диаграммы по закрытый/открытый аккаунт



response = requests.get(
        '{host}/closed/{group_id}'
        .format(host=host, group_id=group_id))

response = response.json()

#создание круговой диаграммы по полу
labels = response['labels']
sizes = response['values']

createPieChart(labels, sizes, 'Closed_accounts')
#создание гистограммы "Топ-5 имен"

response = requests.get(
        '{host}/name/{group_id}'
        .format(host=host, group_id=group_id))

response = response.json()
createBarChart(response,'first_name')
#создание гистограммы "Топ-5 фамилий"
response = requests.get(
        '{host}/surname/{group_id}'
        .format(host=host, group_id=group_id))

response = response.json()
createBarChart(response,'surname')
#создание гистограммы "Топ-5 стран"
response = requests.get(
        '{host}/country/{group_id}'
        .format(host=host, group_id=group_id))

response = response.json()
createBarChart(response,'country')
#создание гистограммы "Топ-5 городов"
response = requests.get(
        '{host}/city/{group_id}'
        .format(host=host, group_id=group_id))

response = response.json()
createBarChart(response,'city')