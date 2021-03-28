import sys
from string_and_bytes import *
from COM_ports import *


def main():
    while True:
        print("XMODEM Python")
        print("Lukasz Janiszewski, Jakub Muszynski")
        print()
        print("Wybierz opcję:\n"
              "1. Rozpocznij program\n"
              "2. Zakończ program")
        wyborUzytkownika = int(input("Twój wybór: "))
        while wyborUzytkownika not in [1, 2]:
            print("Wybrano zla opcje!")
            wyborUzytkownika = int(input("Twój wybór: "))
        if wyborUzytkownika == 2:
            sys.exit()
        print()
        print("Wybierz tryb pracy:\n"
              "1. Wysyłanie\n"
              "2. Odbieranie")
        trybPracy = int(input("Twój wybór: "))
        while trybPracy not in [1, 2]:
            print("Wybrano zla opcje!")
            trybPracy = int(input("Twój wybór: "))
        print()
        connected_ports = available_ports()
        print("Wybierz port:")
        iteration = 1
        if not connected_ports:
            print("BRAK DOSTEPNYCH PORTOW!")
        else:
            for connected_port in connected_ports:
                print(str(iteration) + ". " + str(connected_port))
                iteration += 1
            wybranyPort = int(input("Twój wybór: "))
            while wybranyPort not in range(1, iteration-1):
                print("Wybrano zla opcje!")
                wybranyPort = int(input("Twój wybór: "))
        print()
        print("Z jakiego algorytmu obliczania sumy kontrolnej chcesz skorzystać?\n"
              "1. Domyślny algorytm protokołu Xmodem \n"
              "2. CRC16")
        algorytmSumy = int(input("Twój wybór: "))
        while algorytmSumy not in [1, 2]:
            print("Wybrano zla opcje!")
            algorytmSumy = int(input("Twój wybór: "))
        print()
        print("Wpisz wiadomosc jaka chcesz wyslac:")
        wiadomosc = str(input())
        bytesText = string_to_bytes(wiadomosc)

        # Wywołanie funkcji wysylania i odbierania

        print()
        print()


if __name__ == '__main__':
    main()

