import threading


el = Ele

threads = list()
t = threading.Thread(target=worker)
threads.append(t)
t.start()