import os
import sys
import hashlib
import math
import shutil
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CAT_ARTS = [
    f"""
{Colors.OKCYAN}
   /\\_/\\
  ( o.o )
   > ^ <   Мяу! Я разделитель файлов!
{Colors.ENDC}
""",
    f"""
{Colors.OKGREEN}
  /\\_/\\
 ( ^.^ )
  / > \\   Котик-программист готов к работе!
{Colors.ENDC}
""",
    f"""
{Colors.WARNING}
  /\\_/\\
 ( -.- )
  \\_U_/   Сонный котик ждет файлы для разделения...
{Colors.ENDC}
""",
    f"""
{Colors.OKBLUE}
  /\\_/\\
 ( @ @ )
  (   )   Элитный котик для обработки данных!
{Colors.ENDC}
""",
    f"""
{Colors.HEADER}
  /\\_/\\
 ( ° ° )
  \\_^_/   Котик-хакер шифрует ваши данные!
{Colors.ENDC}
"""
]

def play_sound(sound_type):
    try:
        if sound_type == "select":
            print("\a", end="", flush=True)
        elif sound_type == "success":
            for _ in range(2):
                print("\a", end="", flush=True)
        elif sound_type == "error":
            for _ in range(3):
                print("\a", end="", flush=True)
    except:
        pass

def get_random_cat_art():
    import random
    return random.choice(CAT_ARTS)

def calculate_file_hash(filename, algorithm='md5'):
    hash_func = getattr(hashlib, algorithm)()
    try:
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        print(f"{Colors.FAIL}Ошибка при вычислении хеша: {e}{Colors.ENDC}")
        return None

def verify_file_integrity(original_hash, filename, algorithm='md5'):
    current_hash = calculate_file_hash(filename, algorithm)
    if current_hash == original_hash:
        print(f"{Colors.OKGREEN}✓ Проверка целостности пройдена успешно!{Colors.ENDC}")
        return True
    else:
        print(f"{Colors.FAIL}✗ Ошибка целостности файла! Хеши не совпадают.{Colors.ENDC}")
        return False

def format_file_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def ask_yes_no(question, default=True):
    choices = "Y/n" if default else "y/N"
    answer = input(f"{Colors.BOLD}{question} [{choices}]: {Colors.ENDC}").strip().lower()
    
    if answer == "":
        return default
    return answer in ["y", "yes", "д", "да"]

def safe_move_file(src, dst):
    try:
        shutil.move(src, dst)
        print(f"{Colors.OKGREEN}Файл '{os.path.basename(src)}' перемещен в '{dst}'.{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}Ошибка при перемещении файла '{src}': {e}{Colors.ENDC}")
        return False

def split_file(input_filename, num_parts_str):
    try:
        num_parts = int(num_parts_str)
        if num_parts <= 0:
            print(f"{Colors.FAIL}\nОшибка: Количество частей должно быть больше нуля.{Colors.ENDC}")
            play_sound("error")
            return

        if not os.path.exists(input_filename):
            print(f"{Colors.FAIL}\nОшибка: Файл '{input_filename}' не найден.{Colors.ENDC}")
            play_sound("error")
            return

        base_name, extension = os.path.splitext(input_filename)
        output_folder_name = f"{base_name}_parts"
        
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
            print(f"{Colors.OKGREEN}Создана папка для частей: '{output_folder_name}'{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}Папка '{output_folder_name}' уже существует. Части будут сохранены в неё.{Colors.ENDC}")

        file_size = os.path.getsize(input_filename)
        chunk_size = file_size // num_parts
        remainder = file_size % num_parts

        original_hash = calculate_file_hash(input_filename, 'sha256')
        if original_hash:
            print(f"{Colors.OKCYAN}Хеш исходного файла (SHA-256):{Colors.ENDC} {original_hash}")

        print(f"\n{Colors.HEADER}--- Начинаем разделение файла ---{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Файл:{Colors.ENDC} '{input_filename}'")
        print(f"{Colors.OKBLUE}Размер файла:{Colors.ENDC} {format_file_size(file_size)}")
        print(f"{Colors.OKBLUE}Будет создано:{Colors.ENDC} {num_parts} частей.")

        original_file_in_parts = os.path.join(output_folder_name, os.path.basename(input_filename))
        if safe_move_file(input_filename, original_file_in_parts):
            print(f"{Colors.OKGREEN}Исходный файл перемещен в папку с частями.{Colors.ENDC}")

        with open(original_file_in_parts, 'rb') as f_in:
            for i in range(num_parts):
                output_filename_part = f"{base_name}_part_{i+1:03d}{extension}"
                output_filepath = os.path.join(output_folder_name, output_filename_part)
                
                current_chunk_size = chunk_size
                if i == num_parts - 1:
                    current_chunk_size += remainder
                
                data = f_in.read(current_chunk_size)
                
                with open(output_filepath, 'wb') as f_out:
                    f_out.write(data)
                
                print(f"{Colors.OKCYAN}Создана часть:{Colors.ENDC} '{output_filename_part}'. Размер: {format_file_size(len(data))}.")
        
        print(f"\n{Colors.OKGREEN}--- Готово! Все части файла успешно созданы в папке '{output_folder_name}'. ---{Colors.ENDC}")
        
        info_file = os.path.join(output_folder_name, "!split_info.txt")
        with open(info_file, 'w', encoding='utf-8') as f_info:
            f_info.write(f"Информация о разделении файла\n")
            f_info.write(f"=============================\n")
            f_info.write(f"Исходный файл: {os.path.basename(input_filename)}\n")
            f_info.write(f"Дата разделения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f_info.write(f"Размер исходного файла: {file_size} байт ({format_file_size(file_size)})\n")
            f_info.write(f"Количество частей: {num_parts}\n")
            if original_hash:
                f_info.write(f"Хеш исходного файла (SHA-256): {original_hash}\n")
            f_info.write(f"\nДля объединения частей используйте эту же программу\n")
            f_info.write(f"или команду в командной строке:\n")
            f_info.write(f"copy /b \"{base_name}_part_*{extension}\" \"{os.path.basename(input_filename)}\"\n")
        
        print(f"{Colors.OKGREEN}Создан файл с информацией: '{info_file}'{Colors.ENDC}")
        play_sound("success")

    except ValueError:
        print(f"{Colors.FAIL}\nОшибка: Количество частей должно быть целым числом.{Colors.ENDC}")
        play_sound("error")
    except Exception as e:
        print(f"{Colors.FAIL}\nПроизошла непредвиденная ошибка: {e}{Colors.ENDC}")
        play_sound("error")

def split_by_size(input_filename, chunk_size_str):
    try:
        size_units = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3}
        chunk_size_str = chunk_size_str.upper().replace(' ', '')
        
        unit = ''.join(filter(str.isalpha, chunk_size_str))
        value = ''.join(filter(str.isdigit, chunk_size_str))
        
        if not value:
            raise ValueError("Не указан размер части")
            
        chunk_size = int(value) * size_units.get(unit, 1)
        
        if chunk_size <= 0:
            print(f"{Colors.FAIL}\nОшибка: Размер части должен быть больше нуля.{Colors.ENDC}")
            play_sound("error")
            return

        base_name, extension = os.path.splitext(input_filename)
        output_folder_name = f"{base_name}_parts"
        
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
            print(f"{Colors.OKGREEN}Создана папка для частей: '{output_folder_name}'{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}Папка '{output_folder_name}' уже существует. Части будут сохранены в неё.{Colors.ENDC}")

        file_size = os.path.getsize(input_filename)
        num_parts = math.ceil(file_size / chunk_size)
        
        print(f"\n{Colors.HEADER}--- Начинаем разделение файла по размеру ---{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Файл:{Colors.ENDC} '{input_filename}'")
        print(f"{Colors.OKBLUE}Размер файла:{Colors.ENDC} {format_file_size(file_size)}")
        print(f"{Colors.OKBLUE}Размер части:{Colors.ENDC} {format_file_size(chunk_size)}")
        print(f"{Colors.OKBLUE}Будет создано:{Colors.ENDC} {num_parts} частей.")

        original_hash = calculate_file_hash(input_filename, 'sha256')
        if original_hash:
            print(f"{Colors.OKCYAN}Хеш исходного файла (SHA-256):{Colors.ENDC} {original_hash}")

        original_file_in_parts = os.path.join(output_folder_name, os.path.basename(input_filename))
        if safe_move_file(input_filename, original_file_in_parts):
            print(f"{Colors.OKGREEN}Исходный файл перемещен в папку с частями.{Colors.ENDC}")

        part_num = 1
        with open(original_file_in_parts, 'rb') as f_in:
            while True:
                data = f_in.read(chunk_size)
                if not data:
                    break
                    
                output_filename_part = f"{base_name}_part_{part_num:03d}{extension}"
                output_filepath = os.path.join(output_folder_name, output_filename_part)
                
                with open(output_filepath, 'wb') as f_out:
                    f_out.write(data)
                
                print(f"{Colors.OKCYAN}Создана часть:{Colors.ENDC} '{output_filename_part}'. Размер: {format_file_size(len(data))}.")
                part_num += 1
        
        print(f"\n{Colors.OKGREEN}--- Готово! Все части файла успешно созданы в папке '{output_folder_name}'. ---{Colors.ENDC}")
        
        info_file = os.path.join(output_folder_name, "!split_info.txt")
        with open(info_file, 'w', encoding='utf-8') as f_info:
            f_info.write(f"Информация о разделении файла\n")
            f_info.write(f"=============================\n")
            f_info.write(f"Исходный файл: {os.path.basename(input_filename)}\n")
            f_info.write(f"Дата разделения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f_info.write(f"Размер исходного файла: {file_size} байт ({format_file_size(file_size)})\n")
            f_info.write(f"Размер части: {chunk_size} байт ({format_file_size(chunk_size)})\n")
            f_info.write(f"Количество частей: {part_num-1}\n")
            if original_hash:
                f_info.write(f"Хеш исходного файла (SHA-256): {original_hash}\n")
            f_info.write(f"\nДля объединения частей используйте эту же программу\n")
            f_info.write(f"или команду в командной строке:\n")
            f_info.write(f"copy /b \"{base_name}_part_*{extension}\" \"{os.path.basename(input_filename)}\"\n")
        
        print(f"{Colors.OKGREEN}Создан файл с информацией: '{info_file}'{Colors.ENDC}")
        play_sound("success")

    except Exception as e:
        print(f"{Colors.FAIL}\nПроизошла ошибка: {e}{Colors.ENDC}")
        play_sound("error")

def join_files(parts_folder, output_filename=None):
    try:
        if not os.path.exists(parts_folder):
            print(f"{Colors.FAIL}Папка '{parts_folder}' не существует.{Colors.ENDC}")
            play_sound("error")
            return
        
        all_files = os.listdir(parts_folder)
        
        info_files = [f for f in all_files if f.lower().startswith('!split_info')]
        original_hash = None
        original_filename = None
        
        if info_files:
            info_file = os.path.join(parts_folder, info_files[0])
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "Хеш исходного файла (SHA-256):" in content:
                        original_hash = content.split("Хеш исходного файла (SHA-256):")[1].split('\n')[0].strip()
                    if "Исходный файл:" in content:
                        original_filename = content.split("Исходный файл:")[1].split('\n')[0].strip()
            except:
                pass
        
        if output_filename is None:
            if original_filename:
                output_filename = original_filename
            else:
                if parts_folder.endswith('_parts'):
                    output_filename = parts_folder[:-6]
                else:
                    output_filename = f"restored_{os.path.basename(parts_folder)}"
        
        part_files = []
        original_file_in_parts = None
        
        for f in all_files:
            if f.startswith('!') or f == output_filename:
                continue
            
            if any(x in f for x in ['_part_', '.part', '.001', '.002', '.003']):
                part_files.append(f)
            elif f == original_filename:
                original_file_in_parts = f
                print(f"{Colors.WARNING}Найден исходный файл в папке: '{f}'{Colors.ENDC}")
        
        if not part_files:
            part_files = [f for f in all_files if not f.startswith('!') and f != output_filename and f != original_filename]
        
        if not part_files:
            print(f"{Colors.FAIL}В папке '{parts_folder}' не найдены файлы-части.{Colors.ENDC}")
            play_sound("error")
            return
        
        part_files.sort()
        
        print(f"{Colors.HEADER}--- Начинаем объединение файлов ---{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Найдено частей:{Colors.ENDC} {len(part_files)}")
        print(f"{Colors.OKBLUE}Восстанавливаемый файл:{Colors.ENDC} '{output_filename}'")
        
        total_size = 0
        with open(output_filename, 'wb') as f_out:
            for part_file in part_files:
                part_path = os.path.join(parts_folder, part_file)
                part_size = os.path.getsize(part_path)
                total_size += part_size
                
                print(f"{Colors.OKCYAN}Добавляем часть:{Colors.ENDC} {part_file} ({format_file_size(part_size)})")
                
                with open(part_path, 'rb') as f_in:
                    shutil.copyfileobj(f_in, f_out)
        
        print(f"{Colors.OKCYAN}Общий размер объединенного файла:{Colors.ENDC} {format_file_size(total_size)}")
        print(f"\n{Colors.OKGREEN}--- Готово! Файл успешно объединен: '{output_filename}' ---{Colors.ENDC}")
        
        if original_hash:
            print(f"{Colors.OKCYAN}Проверяем целостности объединенного файла...{Colors.ENDC}")
            if verify_file_integrity(original_hash, output_filename, 'sha256'):
                if ask_yes_no("Удалить папку с частями после успешного объединения?", default=True):
                    try:
                        shutil.rmtree(parts_folder)
                        print(f"{Colors.OKGREEN}Папка '{parts_folder}' успешно удалена.{Colors.ENDC}")
                    except Exception as e:
                        print(f"{Colors.FAIL}Ошибка при удалении папки: {e}{Colors.ENDC}")
        
        play_sound("success")

    except Exception as e:
        print(f"{Colors.FAIL}\nПроизошла ошибка при объединении: {e}{Colors.ENDC}")
        play_sound("error")

def show_help():
    print(f"""
{Colors.HEADER}=== Мяу-Разделитель Файлов - Справка ==={Colors.ENDC}

{Colors.BOLD}Доступные команды:{Colors.ENDC}
  1. Разделить файл на N частей
  2. Разделить файл по размеру части
  3. Объединить части обратно в файл
  4. Показать эту справку
  5. Выход

{Colors.BOLD}Особенности:{Colors.ENDC}
  • Автоматическое перемещение исходного файла в папку с частями
  • Автоматическое определение имени файла при объединении
  • Проверка целостности файлов с помощью SHA-256
  • Создание информационных файлов для легкого восстановления
  • Поддержка больших файлов (до нескольких терабайт)

{Colors.BOLD}Поддерживаемые единицы измерения:{Colors.ENDC}
  B - байты (по умолчанию, если не указано)
  KB - килобайты (1024 байта)
  MB - мегабайты (1048576 байт)
  GB - гигабайты (1073741824 байта)

{Colors.OKGREEN}Примечание: Исходный файл сохраняется в папке с частями для безопасности!{Colors.ENDC}
""")

def list_files_in_current_dir():
    files = [f for f in os.listdir('.') if os.path.isfile(f) and not f.startswith('.')]
    if files:
        print(f"\n{Colors.OKBLUE}Файлы в текущей папке:{Colors.ENDC}")
        for i, f in enumerate(sorted(files), 1):
            size = os.path.getsize(f)
            print(f"  {i:2d}. {f} ({format_file_size(size)})")
    return files

def list_folders_in_current_dir():
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith('.')]
    if folders:
        print(f"\n{Colors.OKBLUE}Папки в текущей папке:{Colors.ENDC}")
        for i, f in enumerate(sorted(folders), 1):
            print(f"  {i:2d}. {f}/")
    return folders

def main_menu():
    while True:
        print(get_random_cat_art())
        print(f"{Colors.HEADER}=== Мяу-Разделитель Файлов ==={Colors.ENDC}")
        
        list_files_in_current_dir()
        list_folders_in_current_dir()
        
        print(f"\n{Colors.BOLD}Выберите действие:{Colors.ENDC}")
        print(f"  1. Разделить файл на N частей")
        print(f"  2. Разделить файл по размеру части")
        print(f"  3. Объединить части обратно в файл")
        print(f"  4. Справка")
        print(f"  5. Выход")
        
        choice = input(f"\n{Colors.BOLD}Ваш выбор (1-5): {Colors.ENDC}")
        play_sound("select")
        
        if choice == '1':
            filename = input(f"{Colors.BOLD}Введите имя файла для разделения: {Colors.ENDC}")
            parts = input(f"{Colors.BOLD}На сколько частей разделить файл? {Colors.ENDC}")
            split_file(filename, parts)
        elif choice == '2':
            filename = input(f"{Colors.BOLD}Введите имя файла для разделения: {Colors.ENDC}")
            chunk_size = input(f"{Colors.BOLD}Размер части (например, 10MB, 500KB, 1GB): {Colors.ENDC}")
            split_by_size(filename, chunk_size)
        elif choice == '3':
            folder = input(f"{Colors.BOLD}Введите папку с частями файла: {Colors.ENDC}")
            output = input(f"{Colors.BOLD}Введите имя результирующего файла (Enter для автоопределения): {Colors.ENDC}")
            if output.strip() == "":
                join_files(folder)
            else:
                join_files(folder, output)
        elif choice == '4':
            show_help()
            input(f"\n{Colors.OKBLUE}Нажмите Enter, чтобы продолжить...{Colors.ENDC}")
            continue
        elif choice == '5':
            print(f"{Colors.OKGREEN}До свидания! Мяу!{Colors.ENDC}")
            play_sound("success")
            break
        else:
            print(f"{Colors.FAIL}Неверный выбор. Пожалуйста, выберите от 1 до 5.{Colors.ENDC}")
            play_sound("error")
        
        input(f"\n{Colors.OKBLUE}Нажмите Enter, чтобы продолжить...{Colors.ENDC}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--split" and len(sys.argv) >= 4:
            split_file(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "--split-size" and len(sys.argv) >= 4:
            split_by_size(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "--join" and len(sys.argv) >= 3:
            output_file = sys.argv[3] if len(sys.argv) >= 4 else None
            join_files(sys.argv[2], output_file)
        elif sys.argv[1] == "--help":
            show_help()
        else:
            print(f"{Colors.FAIL}Неверные аргументы командной строки.{Colors.ENDC}")
            print(f"Использование:")
            print(f"  {sys.argv[0]} --split <файл> <количество_частей>")
            print(f"  {sys.argv[0]} --split-size <файл> <размер_части>")
            print(f"  {sys.argv[0]} --join <папка_с_частями> [результирующий_файл]")
            print(f"  {sys.argv[0]} --help")
    else:
        main_menu()