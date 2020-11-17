from gpio import GPIO
import time


#GPIO.setmode(GPIO.BCM)
#GPIO.setup(26,GPIO.OUT)
#GPIO.setup(19,GPIO.OUT)
#GPIO.setup(13,GPIO.OUT)
#GPIO.setup(6,GPIO.OUT)
#GPIO.setup(5,GPIO.OUT)
#GPIO.setup(11,GPIO.OUT)
#GPIO.setup(9,GPIO.OUT)
#GPIO.setup(10,GPIO.OUT)

#D=[26, 19, 13, 6, 5, 11, 9, 10]
D=[0, 1, 2, 3, 4, 5, 6, 7]



def num2dac(value):
    
    s=[0,0,0,0,0,0,0,0]

    c = bin(value)
    m = 7
    for n in reversed(c):
        if n =='b':
            break
        elif n == "1":
            s[m] = 1
        else:
            s[m] = 0 
        m = m - 1
    
    m = 7
    for n in s:
        if n == 1:
            GPIO.output(D[m], 1)
        else:
            GPIO.output(D[m], 0)
        m = m - 1



while True:
    try:
        number = int(input('Введите число (-1 для выхода):'))
        1/(number+1)
        if number<0 or number>255:
            number=number+'error'
    except(ZeroDivisionError):
        print ('Выход')
        exit()
    except(TypeError):
        print("Число не входит в диапазон")
    else:
       num2dac(number)
       input("для продолжения нажмите enter")
    finally:
        for n in D:
            GPIO.output(n, 0)