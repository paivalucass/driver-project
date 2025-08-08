import os
from fcntl import ioctl
from time import sleep

# TODO: Verificar esse número
RD_PBUTTONS = 24930
DISPLAY_L = 24931

# TODO: Path do driver (verificar)
PATH = '/dev/mydev'

# TODO: Verificar quais valores os botões geram quando pressionados 
BUTTONS_OPTIONS = {
    '0b1110': "UP", 
    '0b1101': "LEFT",
    '0b1011': "RIGHT",
    '0b111': "DOWN",
    '0b1111': "IDLE",
}

# TODO: Verificar quais valores são necessários para mostrar cada número decimal
HEX_0 = 0xC0
HEX_1 = 0xF9
HEX_2 = 0xA4
HEX_3 = 0xB0
HEX_4 = 0x99
HEX_5 = 0x92
HEX_6 = 0x82
HEX_7 = 0xF8
HEX_8 = 0x80
HEX_9 = 0x90
HEX_A = 0x88
HEX_B = 0x83
HEX_C = 0xC6
HEX_D = 0xA1
HEX_E = 0x86
HEX_F = 0x8E

def read_button(fd, show_output_msg):
    ioctl(fd, RD_PBUTTONS)
    button = os.read(fd, 4)
    button = bin(int.from_bytes(button, 'little'))

    if show_output_msg:
        print(f'>>> button {button}')

    return button
    # TODO: Verificar quais valores são necessários para mostrar cada número decimal

def write_display(fd, number):
    """Write a decimal number (0–9) to the 7-segment display."""
    pattern = SEGMENT_MAP.get(number, 0)  # Default 0 if number not found
    ioctl(fd, DISPLAY_L)
    os.write(fd, pattern.to_bytes(4, 'little'))
    

def write_display(fd, ar_num):

    ioctl(fd, DISPLAY_L)

    data = 0
    for num in ar_num:
        data = display_convert(data, num, 8)
    os.write(fd, data.to_bytes(4, 'little'))
    
def display_convert(fd, data, num, ind):
    data = data << ind
    if num == '0':
        data = data | HEX_0
    elif num == '1':
        data = data | HEX_1
    elif num == '2':
        data = data | HEX_2
    elif num == '3':
        data = data | HEX_3
    elif num == '4':
        data = data | HEX_4
    elif num == '5':
        data = data | HEX_5
    elif num == '6':
        data = data | HEX_6
    elif num == '7':
        data = data | HEX_7
    elif num == '8':
        data = data | HEX_8
    elif num == '9':
        data = data | HEX_9
    elif num == 'A':
        data = data | HEX_A
    elif num == 'B':
        data = data | HEX_B
    elif num == 'C':
        data = data | HEX_C
    elif num == 'D':
        data = data | HEX_D
    elif num == 'E':
        data = data | HEX_E
    elif num == 'F':
        data = data | HEX_F
    return data