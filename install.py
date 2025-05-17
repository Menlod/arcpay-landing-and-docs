import os
import shutil
import subprocess

# Пути
source_file = "index.temp.html"
dest_folder = "doc"
dest_file = "index.html"
dest_path = os.path.join(dest_folder, dest_file)

try:
    # Шаг 1: Выполняем mkdocs build
    print("[*] Запускаем mkdocs build...")
    subprocess.run(["mkdocs", "build", "-d", dest_folder], check=True)

    # Шаг 2: Копируем index.temp.html в doc/index.html
    if os.path.exists(source_file):
        shutil.copy(source_file, dest_path)
        print(f"[+] Файл успешно скопирован в {dest_path}")
    else:
        print(f"[!] Ошибка: исходный файл {source_file} не найден.")

except subprocess.CalledProcessError as e:
    print(f"[!] Ошибка при выполнении mkdocs: {e}")
except Exception as e:
    print(f"[!] Произошла ошибка: {e}")