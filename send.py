import socket
import codecs
import time

def getSumScore(file_name):
    with codecs.open(file_name, "r", encoding="utf-8") as f:
        sum_score = float(f.read())
    return sum_score


def main():
    sum_score_file_name = "./data/sum_score.txt"
    host = '192.168.11.13'
    port = 50005
    clientNum = 1

    request_msg = "plz"
    error_msg = "error"
    sum_score = 0
    
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("", port))

    while True:
        serversocket.listen(clientNum)
        conn, addr = serversocket.accept()
        
        while True:
            try:
                msg = conn.recv(1024).decode()
                print("received: ", msg)

                #正しいリクエストメッセージならスコアを送信
                if msg != request_msg:
                    conn.send(error_msg.encode())
                    continue

                sum_score = getSumScore(sum_score_file_name)
                conn.send(str(sum_score).encode())
                time.sleep(0.5)

            except socket.error:
                conn.close()
                break

if __name__ == "__main__":
    main()
