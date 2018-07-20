
from yukari import *
from extract_speech import *


app_name = "C:/Program Files (x86)/AHS/VOICEROID+/YukariEX/VOICEROID.exe"
HOST = "localhost"
PORT = 10500

if __name__ == "__main__":

    if not isVoiceRoidRunning():
        p = subprocess.Popen(app_name)
        time.sleep(10)

    voiceroid = VoiceRoid("VOICEROID＋ 結月ゆかり EX")
    client = start_recognize(HOST, PORT)

    buf = b""
    retrieving = False
    while True:
        buf += client.recv(1)
        if buf.find(b"<RECOGOUT>") != -1 and not retrieving:
            retrieving = True
        elif buf.find(b"</RECOGOUT>") != -1 and retrieving:
            #print(buf.decode("shiftjis"), end="\n\n")
            sentence = extract(buf.decode("shiftjis"))
            print(sentence)
            voiceroid.say(sentence)

            retrieving = False
            buf = b""


