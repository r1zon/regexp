from pprint import pprint
import csv
import re
from operator import itemgetter

with open("phonebook_raw.csv", encoding="utf8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Приведение всех телефонов в формат +7(999)999-99-99 доб.9999
pattern = re.compile(r"(8|\+7)\s*(\(|)(\d{3})(\)|)(\s*|-)(\d{3})(\s*|-)(\d{2})(\s*|-)(\d{2})")
pattern2 = re.compile(r"(\(|)(доб\.)\s*(\d+)(\)|)")
temp_contacts_list = []
for person in contacts_list:
    new_person = []
    for data in person:
        data = pattern.sub(r"+7(\3)\6-\8-\10", data)
        data = pattern2.sub(r"\2\3", data)
        new_person.append(data)
    temp_contacts_list.append(new_person)

# Разделение ФИО по столбцам
for person in temp_contacts_list[1:]:
    if ' ' in person[0]:
        split_person = person[0].split(' ')
        person[0] = split_person[0]
        if len(split_person) == 3:
            if person[2] == '':
                person[2] = split_person[2]
            if person[1] == '':
                person[1] = split_person[1]
        elif len(split_person) == 2:
            if person[1] == '':
                person[1] = split_person[1]
    if ' ' in person[1]:
        split_person = person[1].split(' ')
        person[1] = split_person[0]
        if len(split_person) == 2:
            if person[2] == '':
                person[2] = split_person[1]

new_contacts_list = []
new_contacts_list.append(temp_contacts_list[0])
# Создания списка фамилий в телефонной книге
lastname_list = []
for person in temp_contacts_list[1:]:
    lastname_list.append(person[0])

# Поиск индексов недублируемых фамилий и добавление информации по этим фамилиям в новый список new_contacts_list
add_list = []
not_dubl_index = []
for surname in lastname_list:
    index = lastname_list.index(surname)
    if lastname_list.count(surname) == 1:
        not_dubl_index.append(index+1)
        new_contacts_list.append(temp_contacts_list[index+1])
not_dubl_index.reverse()

# Удаление недублируемых строк
for i in not_dubl_index:
    temp_contacts_list.remove(temp_contacts_list[i])

# Сортировка по фамилии промежуточого списка temp_contacts_list, в котором остались только дубли
temp_contacts_list.remove(temp_contacts_list[0])
temp_contacts_list.sort(key=itemgetter(0))

# Создание одного общего списка add_list из дублей и добавление этого списка в new_contacts_list
while temp_contacts_list != []:
    for i in range(7):
        if temp_contacts_list[0][i] != '':
            add_list.append(temp_contacts_list[0][i])
        elif temp_contacts_list[1][i] != '':
            add_list.append(temp_contacts_list[1][i])
        else:
            add_list.append('')
    new_contacts_list.append(add_list)
    add_list = []
    temp_contacts_list.remove(temp_contacts_list[0])
    temp_contacts_list.remove(temp_contacts_list[0])

with open("phonebook.csv", "w", encoding="utf8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contacts_list)
