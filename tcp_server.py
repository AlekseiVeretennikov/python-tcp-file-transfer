import socket
import hashlib
import os

# Настройки сервера
HOST = 'localhost'
PORT = 65432
BUFFER_SIZE = 4096

def handle_client(conn, addr):

    print(f"[+] Подключен клиент: {addr}")
    try:
      
        received_meta = conn.recv(BUFFER_SIZE).decode()
        if not received_meta or ':' not in received_meta:
            print("[-] Не получены метаданные от клиента. Отключение.")
            return

        filename, expected_hash = received_meta.split(':')
        filename = os.path.basename(filename)
        print(f"[*] Получены метаданные: Имя файла '{filename}', Хэш '{expected_hash[:10]}...'")

        # Отправляем подтверждение клиенту
        conn.sendall(b"META_OK")

   
        sha256 = hashlib.sha256()
        received_path = os.path.join("received_files", filename)
        os.makedirs("received_files", exist_ok=True)

        print(f"[*] Начинаю прием файла...")
        with open(received_path, 'wb') as f:
            while True:
                chunk = conn.recv(BUFFER_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                sha256.update(chunk)

  
        received_hash = sha256.hexdigest()
        print(f"[*] Файл полностью получен. Вычисленный хэш: '{received_hash[:10]}...'")

        if received_hash == expected_hash:
            print("[+] Проверка целостности успешна.")
            conn.sendall(b"FILE_OK")
        else:
            print("[-] ОШИБКА: Проверка целостности не удалась.")
            conn.sendall(b"FILE_CORRUPT")

    except Exception as e:
        print(f"[!] Произошла ошибка при работе с клиентом {addr}: {e}")
    finally:
        print(f"[-] Клиент {addr} отключился.")
        conn.close()

def start_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[*] Сервер запущен и слушает на {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            handle_client(conn, addr)

if __name__ == '__main__':

    start_server()
