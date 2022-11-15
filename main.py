import serial
from terpreter import terpreter
from sx1262 import sx1262

def main():
    print("[+] Type help to View Command Options")
    radio = sx1262()
    while True:
        try:
            text = input('sx1262> ')
        except EOFError:
            break
        if not text:
            continue
        t = terpreter(text, radio)
        try: t.expr()
        except Exception as e:
            print("[+] Exception: ", e)

if __name__ == "__main__":
    main()