import socket
import hashlib
import os
import sys

HOST = 'localhost'
PORT = 65432
BUFFER_SIZE = 4096

def send_file(filename):
    if not os.path.exists(filename):
        print(f"[-] Ошибка: Файл '{filename}' не найден.")
        return


    sha256 = hashlib.sha256()
    print(f"[*] Вычисляю хэш для файла '{filename}'...")
    with open(filename, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            sha256.update(chunk)
    file_hash = sha256.hexdigest()
    print(f"[+] Хэш вычислен: {file_hash[:10]}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
   
            print(f"[*] Подключаюсь к серверу {HOST}:{PORT}...")
            s.connect((HOST, PORT))
            print("[+] Соединение с сервером установлено.")


            basename = os.path.basename(filename)
            s.send(f"{basename}:{file_hash}".encode())

            response = s.recv(BUFFER_SIZE).decode()
            if response != "META_OK":
                print(f"[-] Сервер вернул ошибку на метаданные: {response}")
                return

  
            print(f"[*] Начинаю отправку файла...")
            with open(filename, 'rb') as f:
                while chunk := f.read(BUFFER_SIZE):
                    s.sendall(chunk)
            print("[+] Файл полностью отправлен.")
            s.shutdown(socket.SHUT_WR)

            final_response = s.recv(BUFFER_SIZE).decode()
            if final_response == "FILE_OK":
                print("\n[SUCCESS] Сервер подтвердил, что файл получен корректно!")
            elif final_response == "FILE_CORRUPT":
                print("\n[ERROR] Сервер сообщил, что файл поврежден во время передачи.")
            else:
                print(f"\n[?] Неизвестный ответ от сервера: {final_response}")

        except ConnectionRefusedError:
            print("[-] ОШИБКА: Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
        except Exception as e:
            print(f"[!] Произошла непредвиденная ошибка: {e}")
        finally:
            print("[-] Соединение с сервером закрыто.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_to_send = sys.argv[1]
        send_file(file_to_send)
    else:

        print("Использование: python tcp_client.py <путь_к_файлу>")
