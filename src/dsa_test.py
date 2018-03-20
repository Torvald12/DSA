from tkinter import *
import random

def egcd(a, b):
    mod = b
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return (x + mod) % mod

def powFunc(a, b, m):
    a0 = a
    bits = list(str(format(b, 'b')))
    bits.pop(0)
    i = 0
    while i < len(bits):
        if bits[i] == '0':
            a = (a * a) % m
            i = i + 1
        else:
            a = ((a * a) * a0) % m
            i = i + 1
    return (a)

def Inserting_A():
    Variables()
    Sign()

def Inserting_B():
    Verifying()


def Sign():
    p, q, g, message, has = Variables()
    x = random.getrandbits(32)
    print("x: ", x)
    textBoxSecretKey.config(state=NORMAL)
    textBoxSecretKey.delete('1.0', END)
    textBoxSecretKey.insert(END, hex(x))
    textBoxSecretKey.config(state=DISABLED)

    y = powFunc(g, x, p)
    print("y: ", y)
    textBoxOpenKey.delete('1.0', END)
    textBoxOpenKey.insert(END, hex(y))

    k = random.getrandbits(32)
    print("k: ", k)

    r = (powFunc(g, k, p)) % q
    print("r: ", r)
    textBoxR.delete('1.0', END)
    textBoxR.insert(END, r)

    s = ((egcd(k, q)) * (has + x * r)) % q
    print("s: ", s)
    textBoxS.delete('1.0', END)
    textBoxS.insert(END, s)

    return r, s, y

def Verifying():
    p, q, g, message, has = Variables()

    r = int(textBoxR.get('1.0', END))

    s = int(textBoxS.get('1.0', END))

    y = int(textBoxOpenKey.get('1.0', END), 16)

    w = (egcd(s, q))
    print("w: ", w)
    textBoxW.config(state=NORMAL)
    textBoxW.delete('1.0', END)
    textBoxW.insert(END, w)
    textBoxW.config(state=DISABLED)

    U1 = (has * w) % q
    print("U1: ", U1)

    U2 = (r * w) % q
    print("U2: ", U2)

    v = ((powFunc(g, U1, p) * powFunc(y, U2, p)) % p) % q
    print("v: ", v)
    textBoxV.config(state=NORMAL)
    textBoxV.delete('1.0', END)
    textBoxV.insert(END, v)
    textBoxV.config(state=DISABLED)

    return r

def Check():
    r = Verifying()
    v = int(textBoxV.get('1.0', END))

    if v == r:
        textBoxStatus.delete('1.0', END)
        textBoxStatus.insert(END, "Success!")
    else:
        textBoxStatus.delete('1.0', END)
        textBoxStatus.insert(END, "Error!")

def Variables():
    message = textBoxMessage.get('1.0', END)
    message = message[0:-1]
    textBoxMessage.delete('1.0', END)
    textBoxMessage.insert(END, message)

    has = hash(message)
    if has < 0:
        has = has * (-1)
    print("Hash: ", has)
    textBoxHash.config(state=NORMAL)
    textBoxHash.delete('1.0', END)
    textBoxHash.insert(END, has)
    textBoxHash.config(state=DISABLED)

    p = 168000000000006217
    print("p: ", p)

    q = 1000000000000037
    print("q: ", q)

    g = 159840285456611444
    print("g: ", g)

    return p, q, g, message, has

root = Tk()
root.geometry('550x465+300+200')
root.resizable(width=False, height=False)
root.title("DSA v.1.0.2")

frame_A = Frame(root, bd=2, relief=GROOVE)
frame_B = Frame(root, bd=2, relief=GROOVE)
frame_Message = Frame(root, bd=2, relief=GROOVE)
frame_Status = Frame(root, bd=2, relief=GROOVE)

labelMessage = Label(frame_Message, text="Message:", font="TimesNewRoman 14").pack()
textBoxMessage = Text(frame_Message, width=66, height=1)
textBoxMessage.insert(END, "Input message, please...")
textBoxMessage.pack()

labelHash = Label(frame_Message, text="Hash:", font="TimesNewRoman 14").pack()
textBoxHash = Text(frame_Message, width=32, height=1)
textBoxHash.pack()

labelSecretKey = Label(frame_A, text="Side A", font="TimesNewRoman 16").pack()
labelSecretKey = Label(frame_A, text="Secret key:", font="TimesNewRoman 14").pack()
textBoxSecretKey = Text(frame_A, width=32, height=1)
textBoxSecretKey.pack()

labelW = Label(frame_B, text="Side B", font="TimesNewRoman 16").pack()
labelOpenKey = Label(frame_B, text="Open key:", font="TimesNewRoman 14").pack()
textBoxOpenKey = Text(frame_B, width=32, height=1)
textBoxOpenKey.pack()

labelR = Label(frame_A, text="R:", font="TimesNewRoman 14").pack()
textBoxR = Text(frame_A, width=32, height=1)
textBoxR.pack()

labelS = Label(frame_A, text="S:", font="TimesNewRoman 14").pack()
textBoxS = Text(frame_A, width=32, height=1)
textBoxS.pack()

labelW = Label(frame_B, text="W:", font="TimesNewRoman 14").pack()
textBoxW = Text(frame_B, width=32, height=1)
textBoxW.pack()

labelV = Label(frame_B, text="V:", font="TimesNewRoman 14").pack()
textBoxV = Text(frame_B, width=32, height=1)
textBoxV.pack()

labelStatus = Label(frame_Status, text="Status:", font="TimesNewRoman 14").pack()
textBoxStatus = Text(frame_Status, width=66, height=1)
textBoxStatus.pack()

frame_Message.place(x = 10, y = 10)
frame_A.place(x = 10, y = 130)
frame_B.place(x = 280, y = 130)
frame_Status.place(x = 10, y = 400)

buttonSign = Button(frame_A, width=12, height=2, fg="black", command=Inserting_A)
buttonSign["text"] = "Sign"
buttonSign.pack()

buttonVerify = Button(frame_B, width=12, height=2, fg="black", command=Inserting_B)
buttonVerify["text"] = "Verify"
buttonVerify.pack()

buttonCheck = Button(root, width=15, height=2, fg="black", command=Check)
buttonCheck["text"] = "Check"
buttonCheck.place(x = 220, y = 352)

root.mainloop()
