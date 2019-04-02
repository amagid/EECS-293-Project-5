#!/usr/bin/python3

from radio.radio import Radio
import io

if __name__ == '__main__':
    
    radio = Radio()
    result = radio.attempt_connect()
    print(result)