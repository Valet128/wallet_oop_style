from io import StringIO
from main import Wallet

wallet = Wallet()

class TestWallet():

    def test_add_note(self):
        # успешные проверки
        assert wallet.add_note(StringIO('1'), StringIO('101'), StringIO("desc2")) == "Запись успешно добавлена!"
        assert wallet.add_note(StringIO('1'), StringIO('123'), StringIO("")) == "Запись успешно добавлена!"
        assert wallet.add_note(StringIO('1'), StringIO('-1'), StringIO("desc2")) == "Запись успешно добавлена!"

        # неуспешные проверки 1 аргумент

        assert wallet.add_note(StringIO('0'), StringIO('101'), StringIO("desc2")) == "Операция отменена!"
        assert wallet.add_note(StringIO('3'), StringIO('101'), StringIO("desc2")) == "Вы ввели некорректные данные!"
        assert wallet.add_note(StringIO('ываы'), StringIO('101'), StringIO("desc2")) == "Вы ввели некорректные данные!"
        assert wallet.add_note(StringIO(''), StringIO('101'), StringIO("desc2")) == "Вы ввели некорректные данные!"
        assert wallet.add_note(StringIO('-1'), StringIO('101'), StringIO("desc2")) == "Вы ввели некорректные данные!"

        # неуспешные проверки 2 аргумент

        assert wallet.add_note(StringIO('1'), StringIO('кк'), StringIO("desc2")) == "Вы ввели некорректные данные!"
        assert wallet.add_note(StringIO('1'), StringIO(''), StringIO("desc2")) == "Вы ввели некорректные данные!"
        
        
        
        
        