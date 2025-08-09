#!/usr/bin/python3

import os, sys, time
from fcntl import ioctl

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

# 7-seg encoding (common mapping used on Altera/Intel boards)
# Index = digit, Value = segments (gfedcba)
DIGIT_7SEG = [
    0x3F, # 0
    0x06, # 1
    0x5B, # 2
    0x4F, # 3
    0x66, # 4
    0x6D, # 5
    0x7D, # 6
    0x07, # 7
    0x7F, # 8
    0x6F, # 9
]
BLANK = 0x00


def encode_number_to_4digits(n: int) -> bytes:
    """Return 4 bytes (little-endian digit order: least significant digit first)
    for the right 4 displays. Leading positions are blank.
    """
    n = max(0, n)
    digits = []
    v = n
    for i in range(4):
        if v > 0 or i == 0:
            d = v % 10
            digits.append(DIGIT_7SEG[d])
            v //= 10
        else:
            digits.append(BLANK)
    return bytes(digits)  # [d0, d1, d2, d3] (LS digit first)


def write_right_display(fd: int, data4: bytes) -> None:
    ioctl(fd, WR_R_DISPLAY)
    os.write(fd, data4)


def clear_left_display(fd: int) -> None:
    ioctl(fd, WR_L_DISPLAY)
    os.write(fd, bytes([BLANK, BLANK, BLANK, BLANK]))


def read_pushbuttons(fd: int) -> int:
    """Read raw pushbutton state (bitmask). Non-zero when any button is pressed."""
    ioctl(fd, RD_PBUTTONS)
    raw = os.read(fd, 4)
    return int.from_bytes(raw, 'little')


def main():
    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>" % sys.argv[0])
        exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)

    try:
        # Initialize display with 0 and clear left side
        count = 0
        write_right_display(fd, encode_number_to_4digits(count))
        clear_left_display(fd)

        last_pressed = False
        while True:
            btn = read_pushbuttons(fd)
            pressed = (btn != 0)
            # On rising edge (click): increment and update display
            if pressed and not last_pressed:
                count = (count + 1) % 10000  # wraps at 9999 -> 0
                write_right_display(fd, encode_number_to_4digits(count))
                print(f"Display: {count:04d}")
            last_pressed = pressed
            # Simple debounce/poll interval
            time.sleep(0.02)
    except KeyboardInterrupt:
        pass
    finally:
        os.close(fd)


if __name__ == '__main__':
    main()

