# coding utf-8
import re
import socket


def extract(text):
    text = "".join(text.split()) # REMOVE CRLF
    pattern = r"<RECOGOUT>.*</RECOGOUT>"

    m = re.search(pattern, text)
    if m is None:
        #print("\n\nNONE\n\n")
        print(text)
        return
        #raise ValueError("RECOGOUT not found")
    recogout = m.group()
    #print("\n\nnot NONE\n\n")

    words = re.findall(r"WORD=\"([^\"]+)\"", recogout)
    sentence = ""
    if words is not None:
        for word in words:
            sentence += word
    return sentence


def start_recognize(HOST, PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    return client

