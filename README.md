# Xmodem

## Table of Content
* [General Info](#general-info)
* [Technologies](#technologies)
* [Status](#status)
* [Requirements](#requirements)
* [Description](#description)


## General info
Xmodem protocol project in Python with GUI, using default checksum and(or) CRC16 checksum


## Technologies
* Python
* Pycharm
* PyQt5


## Status
Finished


## Requirements
NONE


## Description
Problemem zadania było napisanie programu implementującego protokół Xmodem w wersjach z domyślną sumą kontrolną i CRC16.
Zaimplementowanego przez nas algorytmu używa się przy pomocy interfejsu graficznego, który umożliwia wybranie pliku, na
którym chcemy operować. Do działania na portach użyliśmy programu Virtual Serial Port Tools, który umożliwił tworzenie
wirtualnych portów, wykorzystywanych dalej w programie. Działanie protokołu sprawdziliśmy przy użyciu programu HyperACCESS,
czyli nowszej wersji HyperTerminala. Użytkownik na samym początku wybiera czy chce wysłać czy odebrać wiadomość, port z
dostępnych (COM1 i COM2), następnie algorytm obliczania sumy kontrolnej i na samym końcu podaje plik, który chce wysłać lub
plik do którego chce zapisać odebraną zawartość, w zależności od wybranej pierwszej opcji.
Algorytm działa następująco:
1. W zależności od wybranego algorytmu odbiorca wysyła do nadawcy znak „C” (gdy został wybrany CRC16) lub flagę „NAK”
(gdy został wybrany domyślny algorytm protokołu Xmodem)
2. Nadawca zaczyna następnie wysyłać pakiety danych złożone z 133 bajtów (132 bajtów w przypadku domyślnego
algorytmu sumy kontrolnej) (1. Bajt – nagłówek, 2. i 3. Bajt – numer pakietu, bajty 4-131 – przesyłane dane, bajty 132-
133 – obliczona suma kontrolna)
3. Za każdym razem odbiorca po odebraniu pakietu oblicza sumę kontrolną na nowo, porównuje ją z sumą kontrolną zawartą
w pakiecie i wysyła flagę „ACK” gdy obie sumy są równe lub „NAK” gdy nie są równe. W pierwszym przypadku nadawca
wysyła kolejny pakiet, w drugim przypadku nadawca jeszcze raz przesyła ostatni pakiet
4. Gdy nadawca nie ma już pakietów do wysłania wysyła flagę „EOT”, co oznacza, że nie ma już żadnych danych do wysłania.
Odbiorca odsyła następnie flagę „ACK”. Transmisja jest w tym momencie zakończona.
