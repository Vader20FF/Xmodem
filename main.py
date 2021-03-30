import sys
from string_and_bytes import *
from COM_ports import *
from communication import *


def main():
    coms = inicialize_ports()
    while True:
        print("XMODEM Python")
        print("Lukasz Janiszewski, Jakub Muszynski")
        print()
        print("Wybierz opcję:\n"
              "1. Rozpocznij program\n"
              "2. Zakończ program")
        wybor_uzytkownika = int(input("Twój wybór: "))
        while wybor_uzytkownika not in [1, 2]:
            print("Wybrano zla opcje!")
            wybor_uzytkownika = int(input("Twój wybór: "))
        if wybor_uzytkownika == 2:
            sys.exit()
        print()
        connected_ports = available_ports()
        print("Wybierz port nadawcy:")
        iteration = 1
        if not connected_ports:
            print("BRAK DOSTEPNYCH PORTOW!")
        else:
            for connected_port in connected_ports:
                print(str(iteration) + ". " + str(connected_port))
                iteration += 1
            wybrany_port = int(input("Twój wybór: "))
            while wybrany_port not in range(1, iteration):
                print("Wybrano zla opcje!")
                wybrany_port = int(input("Twój wybór: "))
            if wybrany_port == 1:
                port_nadawcy, port_odbiorcy = coms
            else:
                port_odbiorcy, port_nadawcy = coms
        print()
        print("Z jakiego algorytmu obliczania sumy kontrolnej chcesz skorzystać?\n"
              "1. Domyślny algorytm protokołu Xmodem \n"
              "2. CRC16")
        algorytm_sumy = int(input("Twój wybór: "))
        while algorytm_sumy not in [1, 2]:
            print("Wybrano zla opcje!")
            algorytm_sumy = int(input("Twój wybór: "))
        if algorytm_sumy == 2:
            crc = True
        else:
            crc = False
        print()
        print("Wpisz wiadomosc jaka chcesz wyslac:")
        wiadomosc = str(input())
        bytesText = string_to_bytes(wiadomosc)

        # Rozpoczecie komunikacji
        start_communication(bytesText, crc, port_nadawcy, port_odbiorcy)

        # port_nadawcy.close()
        # port_odbiorcy.close()

        print()
        print()


if __name__ == '__main__':
    main()

