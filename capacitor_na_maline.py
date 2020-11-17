import RPi.GPIO as GPIO;
import time as t;
import numpy as np;
import matplotlib.pyplot as plt;

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)

GPIO.setup(22, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(14, GPIO.IN)
GPIO.setup(3, GPIO.IN)
GPIO.setup(2, GPIO.IN)

D = [26, 19, 13, 6, 5, 11, 9, 10]
D2 = [21, 20, 16, 12, 7, 8, 25, 24]


def num2pins(pins, v):
    #    D = [26, 19, 13, 6, 5, 11, 9, 10]
    #   D2 = [21, 20, 16, 12, 1, 7, 8, 25]
    # D = [0, 1, 2, 3, 4, 5, 6, 7]
    s = [0, 0, 0, 0, 0, 0, 0, 0]

    value = int(v)
    c = bin(value)
    p = 7
    for i in reversed(c):
        if i == 'b':
            break
        elif i == "1":
            s[p] = 1
        else:
            s[p] = 0
        p = p - 1

    p = 0
    for i in s:
        if i == 1:
            GPIO.output(pins[p], 1)
        else:
            GPIO.output(pins[p], 0)
        p = p + 1


def adc_procedure():  # поиск дихотомией
    middle = 128
    value = 128
    while middle > 0:
        # print(middle, value)
        middle /= 2
        # print(value)
        num2pins(D, value)
        num2pins(D2, value)
        print("4", GPIO.input(4))
        print("22", GPIO.input(22))
        print("27", GPIO.input(27))
        print("18", GPIO.input(18))
        print("15", GPIO.input(15))
        print("14", GPIO.input(14))
        print("3", GPIO.input(3))
        print("2", GPIO.input(2))
        if GPIO.input(4) == 1:
            # if value > 200:
            value -= middle
        else:
            value += middle
        print(value)
        if value >= 255:
            # break
            value = 0
            middle = 0

    print("exit", value * 3.3 / 256)
    input()
    return value * 3.3 / 256


try:
    listV = []  # для напряжения
    listT = []  # для времени

    while adc_procedure() > 0:
        GPIO.output(17, 0)
        print("wait")
        t.sleep(0.1)

    print("new block", GPIO.input(4))
    print("22", GPIO.input(22))
    print("27", GPIO.input(27))
    print("18", GPIO.input(18))
    print("15", GPIO.input(15))
    print("14", GPIO.input(14))
    print("3", GPIO.input(3))
    print("2", GPIO.input(2))
    input()
    num2pins(D, 255)
    num2pins(D2, 255)
    print("C high", GPIO.input(4))
    print("22", GPIO.input(22))
    print("27", GPIO.input(27))
    print("18", GPIO.input(18))
    print("15", GPIO.input(15))
    print("14", GPIO.input(14))
    print("3", GPIO.input(3))
    print("2", GPIO.input(2))
    input()
    t_start = t.time()
    GPIO.output(17, 1)

    while True:
        listV.append(adc_procedure())
        listT.append(t.time() - t_start)
        # t.sleep(0.1)
        print(listV)
        if listV[-1] >= 200:
            break

    GPIO.output(17, 0)
    while listV[-1] > 0:
        listV.append(adc_procedure())
        listT.append(t.time() - t_start)

    measure = listV
    plt.plot(measure)
    plt.show()
    np.savetxt('data.txt', measure, fmt='%d')
    print("save")

    dT = (listT[-1] - listT[0]) / (len(listT) - 1)
    dV = (listV[-1] - listV[0]) / (len(listV) - 1)
    listDelta = []
    listDelta.append(dT)
    listDelta.append(dV)
    np.savetxt('settings.txt', listDelta, fmt='%d')

finally:  # сброс настроек
    for i in D:
        GPIO.output(i, 0)
    for j in D2:
        GPIO.output(j, 0)

