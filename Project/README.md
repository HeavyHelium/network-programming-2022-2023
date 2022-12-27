# Network Programming Project: Parallel Quicksort Client-Server
## **Тема: паралелен quicksort/selection sort**

1. Клиентът подава **входни данни**\:
* брой процеси

* масивът, който ще бъде сортиран

2. Сървърът\: 
* изпълнява алгоритъма върху входните данни

* връща резултата на Клиента

* Сървърът е multithreaded, т.е няколко клиенти да могат едновременно да правят заявки към сървъра.

Направено е сравнение между паралелния вариант на quicksort и последователния.

## How to run the project
While in the Project diretory\:

* Start the server\:

```sh
python3 src/server.py
```

* In order for a client to connect to server

```sh
python3 src/client.py
```

Multiple clients can be connected to the server and send their queries. This can be achieved by running the client script from multiple terminals.