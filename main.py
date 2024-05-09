import os
import datetime
import json
from sys import stdin
from io import StringIO


# проверка на наличие папки wallets если нет то создаем, также сразу добавляем путь к располжению исполняемого файла
file = os.path.realpath(__file__)
path = os.path.dirname(file)
wallets_path = path+'/wallets'
check_folder = os.path.isdir(wallets_path)

if not check_folder:
    os.mkdir(wallets_path)

# В данном коде много семантики, поэтому аннотации к каждой переменной являются излишни.    
# Класс кошелька для работы с данными 

class Wallet:   
    balance = 0
    incomes = 0
    expenses = 0
    all_notes = []
    new_note = {}

    def __init__(self):
        wallets_number = len(os.listdir(wallets_path))
        print(wallets_path)
        if wallets_number == 0:
            with open(f'{wallets_path}/wallet.json', 'w', encoding='utf-8') as file:
                print('Новый кошелек создан.')
        else:
            if os.stat(f'{wallets_path}/wallet.json').st_size > 0:
                with open(f'{wallets_path}/wallet.json', 'r', encoding='utf-8') as file:
                    self.all_notes = json.load(file)
                    print("Ваши записи: ")
                    if len(self.all_notes) == 0:
                        print("В вашем кошельке нет ни одной записи!")
                    else:
                        for note in self.all_notes:
                            print(note)
                    print('Ваш кошелек открыт.')
            else:
                print("Добавьте новую запись с помощью команды.")

    def add_note(self, category:str=stdin, amount:str=stdin, description:str=stdin) -> str:
        try:
            if isinstance(category, StringIO) and isinstance(amount, StringIO) and isinstance(description, StringIO):
                category = int(category.readline())
                if category == 1:
                    category = 'Доход'
                elif category == 2:
                    category = 'Расход'
                elif category == 0:
                    print('Операция отменена!')
                    return 'Операция отменена!'
                else:
                    print('Операция отменена!')
                    raise ValueError('Некорректные данные!')
                amount = abs(int(amount.readline()))
                description = description.readline()
            else:
                category = int(input("Введите категорию: 1=Доход, 2=Расход, 0=Отмена: "))
                if category == 1:
                    category = 'Доход'
                elif category == 2:
                    category = 'Расход'
                else: 
                    print('Операция отменена!')
                    raise
                amount = abs(int(input("Введите сумму: ")))
                description = input("Введите описание: ")
            
            if len(self.all_notes) > 0:
                id = self.all_notes[0]['id']
                for note in self.all_notes:
                    if id <= note['id']:
                        id = note['id']+1
            else:
                id = 1 
                
            self.new_note['id'] = id
            self.new_note['category'] = category
            self.new_note['amount'] = amount
            self.new_note['description'] = description
            self.new_note['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            self.all_notes.append(self.new_note)
            self.new_note = {}

            with open(f'{wallets_path}/wallet.json', 'w', encoding='utf-8') as file:
                json.dump(self.all_notes, file, indent=4, ensure_ascii=False)
            print('Запись успешно добавлена!')
            return 'Запись успешно добавлена!'
        except Exception as e:
            print("Вы ввели некорректные данные!", e)
            return "Вы ввели некорректные данные!"
            
    def get_balance(self):
        if len(self.all_notes) > 0:
            incomes_amount = 0
            expenses_amount = 0
            for note in self.all_notes:
                if note['category'].lower() == 'Доход'.lower():
                    incomes_amount += note['amount']
                else:
                    expenses_amount += note['amount']
            balance = incomes_amount - expenses_amount
            print(f"Баланс: {balance} руб.")
        else:
            print("Баланс: 0 руб.")

    def show_all_incomes(self):
        if len(self.all_notes) > 0:
            incomes_amount = 0
            for note in self.all_notes:
                if note['category'].lower() == 'Доход'.lower():
                    incomes_amount += note['amount']
            print(f"Доходы: {incomes_amount} руб.")
        else:
            print("Доходы: 0 руб.")

    def show_all_expenses(self):
        if len(self.all_notes) > 0:
            expenses_amount = 0
            for note in self.all_notes:
                if note['category'].lower() == 'Расход'.lower():
                    expenses_amount += note['amount']
            print(f"Расходы: {expenses_amount} руб.")
        else:
            print("Расходы: 0 руб.")

    def edit_note(self):
        try:
            id = int(input("Введите ID записи (0 = Отмена): "))
            if id == 0:
                print('Операция отменена!')
                raise
            else:
                
                with open(f'{wallets_path}/wallet.json', 'r', encoding='utf-8')as file:
                    self.all_notes = json.load(file)
                    
                if len(self.all_notes) > 0:
                    exist_id = False
                    for note in self.all_notes:
                        if id == note['id']:
                            exist_id = True
                            try:
                                category = int(input("Исправьте категорию: 1=Доход, 2=Расход, 0=Отмена: "))
                                if category == 1:
                                    category = 'Доход'
                                elif category == 2:
                                    category = 'Расход'
                                else: 
                                    print('Операция отменена!')
                                    raise
                                amount = int(input("Исправьте сумму: "))
                                description = input("Исправьте описание: ")
                                note['category'] = category
                                note['amount'] = amount
                                note['description'] = description
                                note['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                                with open(f'{wallets_path}/wallet.json', 'w', encoding='utf-8') as file:
                                    json.dump(self.all_notes, file, indent=4, ensure_ascii=False)

                                print('Запись успешно отредактирована!')
                                break
                            except:
                                print("Вы ввели некорректные данные!")
                                break
                    if exist_id == False:
                        print("Такой записи не существует!")
                else:
                    print("В кошельке нет ни одной записи!")
        except:
            print("Вы ввели некорректные данные!")

    def delete_note(self):
        try:
            id = int(input("Введите ID записи (0 = Отмена): "))
            if id == 0:
                print('Операция отменена!')
                raise
            else:
                with open(f'{wallets_path}/wallet.json', 'r', encoding='utf-8')as file:
                    self.all_notes = json.load(file)
                if len(self.all_notes) > 0:
                    exist_id = False
                    for note in self.all_notes:
                        if id == note['id']:
                            exist_id = True
                            self.all_notes.remove(note)

                            with open(f'{wallets_path}/wallet.json', 'w', encoding='utf-8') as file:
                                json.dump(self.all_notes, file, indent=4, ensure_ascii=False)

                            print("Запись успешно удалена!")
                            break
                    if exist_id == False:
                        print("Такой записи не существует!")
                else:
                    print("В кошельке нет ни одной записи!")
        except:
            print("Вы ввели некорректные данные!")

    def show_all_notes(self):
        if len(self.all_notes) > 0:
            for note in self.all_notes:
                print(note)
        else:
            print("В кошельке нет ни одной записи!")

    
def main():
    app_run = True
    print("""
    #   Команды для приложения:
    - Выход - 0
    - Добавить запись - 1
    - Узнать баланс - 2  
    - Сумма Доходов - 3
    - Сумма Расходов - 4
    - Редактировать запись - 5
    - Удалить запись - 6
    - Показать все записи - 7
    """)
    wallet = Wallet()
    
    while app_run:
        try:
            command = int(input("Введите команду: "))
            if command == 0:
                print("Закрытие приложения...")
                break
            elif command == 1:
                wallet.add_note()
            elif command == 2:
                wallet.get_balance()
            elif command == 3:
                wallet.show_all_incomes()
            elif command == 4:
                wallet.show_all_expenses()
            elif command == 5:
                wallet.edit_note()
            elif command == 6:
                wallet.delete_note()
            elif command == 7:
                wallet.show_all_notes()
            
        except Exception as e:
            print("Вы ввели некорректные данные!", e)
            
#   Команды для приложения:
# Добавить запись - 1
# Узнать баланс - 2  
# Сумма Доходов - 3
# Сумма Расходов - 4
# Редактировать запись - 5
# Удалить запись - 6
# Показать все записи - 7
# 
# 
# проверка на текущий модуль     
if __name__ == "__main__":
    main()



