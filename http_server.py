import socket

HOST = 'localhost'
PORT = 65432

# --- ШАГ 1: СОЗДАЕМ ОБЫЧНЫЕ СТРОКИ (не байтовые) ---

# Убираем префикс b""" и работаем с обычным текстом.
# Теперь Python не ругается на русские буквы.
html_200_ok_text = """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Connection: close

<!DOCTYPE html>
<html>
<head>
    <title>Веб-сервер</title>
</head>
<body>
    <h1>Привет, мир, от моего сервера на Python!</h1>
    <p>Этот сервер понимает HTTP.</p>
</body>
</html>
"""

html_404_not_found_text = """HTTP/1.1 404 Not Found
Content-Type: text/html; charset=utf-8
Connection: close

<!DOCTYPE html>
<html>
<head>
    <title>Ошибка 404</title>
</head>
<body>
    <h1>404 - Страница не найдена</h1>
    <p>Запрошенный вами ресурс не существует на этом сервере.</p>
</body>
</html>
"""

def start_web_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[*] ВЕБ-СЕРВЕР запущен и слушает на http://{HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"[+] Подключился веб-клиент (браузер): {addr}")
                request = conn.recv(1024).decode(errors='ignore') # Добавили 'ignore' для стабильности
                print("--- Запрос от браузера ---")
                print(request.strip())
                print("--- Конец запроса ---")

                if request.startswith('GET / HTTP/1.1'):
                    print("[>] Отправляю ответ 200 OK")
                    # --- ШАГ 2: КОДИРУЕМ ТЕКСТ В БАЙТЫ ПЕРЕД ОТПРАВКОЙ ---
                    conn.sendall(html_200_ok_text.encode('utf-8'))
                else:
                    print("[>] Отправляю ответ 404 Not Found")
                    # --- И ЗДЕСЬ ТОЖЕ КОДИРУЕМ ---
                    conn.sendall(html_404_not_found_text.encode('utf-8'))


if __name__ == '__main__':
    start_web_server()