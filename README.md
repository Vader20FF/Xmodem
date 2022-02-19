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
* Pyserial module
* PyQt5
* HyperACCESS


## Status
Finished


## Requirements
* newest version of python environment
* pyserial
* HyperACCESS
* Virtual Serial Port Tool


## Description
The task was to write an app implementing Xmodem protocol both with version with default checksum and the CRC16. 
Our program is used with a help of GUI, in which the user is able to choose the file on which we want to operate.
For virtual COM ports creation we used Virtual Serial Port Tool. The correctness of pure implementation of protocol we checked with help of HyperACCESS program which is the newer version of HyperTerminal.

At the beginning user chooses:
* if he want to send or receive message, 
* available port (COM1 and COM2)
* default checksum or CRC16
* file which he would like to send (or name of the file which he would like to receive the data into)

The algorithm works in the following way:
1. Depending on the checksum, that has been chosen, the receiver sends "C" sign (CRC16) or "NAK" flag (default checksum)
2. Sender starts to send data packets consisting of 133 bytes (132 bytes if default checksum was chose). 1 byte is header, 2 and 3 bytes are packet number, bytes 4-131 are the data which is being send, bytes 132-133 are the calculated checksum
3. Every time the packet is received, the receiver calculated checksum and compares it with the checksum included in the packet. If both checksums are equal he sends "ACK" flag, if they are not the "NAK" flag is sent. In the first case, the sender continues data transfer. Otherwise the sender asks for the last packet to be sent again.
4. If sender do not have any packets to be send left he sends "EOT" flag. The receiver responds with "ACK" flag and the transmission is closed in this moment.
