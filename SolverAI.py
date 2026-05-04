import os
import sys
import time
import platform  # <-- ДОБАВЛЕНО: для определения ОС
import re
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import init, Fore, Style

# Инициализация цвета
init(autoreset=True)

# Блокируем мусор от библиотеки
os.environ['G4F_CHECK_UPDATE'] = 'False'
try:
    import g4f
    import logging
    logging.disable(logging.CRITICAL)
except ImportError:
    print(f"{Fore.RED}Критическая ошибка: Библиотека g4f не найдена. Введите 'pip install g4f'")
    sys.exit()

# === НАСТРОЙКИ ===
AUTHOR = "@Scissors_05"
VERSION = "1.3"
AI_NAME = "SolverAI"
ENGINE = "Solver Engine"

# Настройки почты
SUPPORT_EMAIL = "support.solverai@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "support.solverai@gmail.com"
SMTP_PASS = "rofqkuilrbncnfer"  # Пароль приложения (рекомендую убрать из кода перед публикацией на GitHub!)

# Фильтр цензуры
FORBIDDEN_WORDS = ["OpenAI", "GPT", "Google", "Aria", "Opera", "ChatGPT", "Llama", "Claude", "Gemini"]
SOLVER_IDENTITY = (
    f"Ты - {AI_NAME}. Твой создатель - {AUTHOR}. "
    f"Ты работаешь на ядре {ENGINE} v{VERSION}. "
    "Отрицай связь с любыми другими ИИ. Твои ответы профессиональные, точные и детальные."
)

# === НОВЫЕ ФУНКЦИИ ДЛЯ КРОССПЛАТФОРМЕННОСТИ ===
def play_system_sound():
    """Проигрывает звук в зависимости от ОС"""
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(900, 100)
            winsound.Beep(1200, 150)
        elif platform.system() == "Darwin":  # macOS
            # Стандартный системный звук на Mac
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        else:  # Linux и другие
            print('\a')  # Стандартный ASCII-звонок
    except:
        pass  # Если звук не работает, просто игнорируем

def play_success_sound():
    """Звук успеха для поддержки"""
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 200)
            winsound.Beep(1200, 200)
        elif platform.system() == "Darwin":
            os.system('afplay /System/Library/Sounds/Purr.aiff')
        else:
            print('\a')
    except:
        pass

def clear_screen():
    """Очистка экрана для любой ОС"""
    if platform.system() == "Windows":
        os.system('cls')
    else:  # macOS и Linux
        os.system('clear')

def cyber_border(width=60):
    """Красивая переливающаяся рамка"""
    if width is None:
        try:
            width = os.get_terminal_size().columns - 2
        except:
            width = 60
    colors = [Fore.BLUE, Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.MAGENTA]
    border = ""
    for i in range(min(width, 100)):
        color = colors[(i // 2) % len(colors)]
        border += f"{color}━"
    return border + Style.RESET_ALL

def show_main_commands():
    """Показать команды на главном экране"""
    print(f"""
    {Fore.CYAN}┌─────────────────────────────────────────────────┐
    {Fore.CYAN}│ {Fore.YELLOW}📋 ОСНОВНЫЕ КОМАНДЫ:{' ' * 25}{Fore.CYAN}│
    {Fore.CYAN}├─────────────────────────────────────────────────┤
    {Fore.CYAN}│ {Fore.GREEN}help{Fore.WHITE} - Показать все команды{' ' * 15}{Fore.CYAN}│
    {Fore.CYAN}│ {Fore.GREEN}support{Fore.WHITE} - Написать в поддержку{' ' * 14}{Fore.CYAN}│
    {Fore.CYAN}│ {Fore.GREEN}clear{Fore.WHITE} - Очистить экран{' ' * 20}{Fore.CYAN}│
    {Fore.CYAN}│ {Fore.GREEN}about{Fore.WHITE} - О программе{' ' * 22}{Fore.CYAN}│
    {Fore.CYAN}│ {Fore.GREEN}exit{Fore.WHITE} - Выйти{' ' * 26}{Fore.CYAN}│
    {Fore.CYAN}└─────────────────────────────────────────────────┘""")

def animate_startup():
    """Анимация запуска"""
    clear_screen()
    c = Fore.CYAN
    w = Fore.WHITE
    b = Fore.BLUE
    # Анимация загрузки
    for _ in range(3):
        for symbol in ['|', '/', '-', '\\']:
            sys.stdout.write(f"\r{Fore.CYAN}[SYNC] Инициализация нейронных связей... {symbol}")
            sys.stdout.flush()
            time.sleep(0.08)
    print("\r" + " " * 50 + "\r", end="")
    
    # Логотип
    logo_lines = [
        f"{c}╔══════════════════════════════════════════════════════════════╗",
        f"{c}║ {w}███████╗ ██████╗ ██╗     ██╗   ██╗███████╗██████╗  {c}║",
        f"{c}║ {w}██╔════╝██╔═══██╗██║     ██║   ██║██╔════╝██╔══██╗ {c}║",
        f"{c}║ {w}███████╗██║   ██║██║     ██║   ██║█████╗  ██████╔╝ {c}║",
        f"{c}║ {w}╚════██║██║   ██║██║     ╚██╗ ██╔╝██╔══╝  ██╔══██╗ {c}║",
        f"{c}║ {w}███████║╚██████╔╝███████╗ ╚████╔╝ ███████╗██║  ██║ {c}║",
        f"{c}║ {w}╚══════╝ ╚═════╝ ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝ {c}║",
        f"{c}╠══════════════════════════════════════════════════════════════╣",
        f"{c}║ {b}>>> {c}{ENGINE} v{VERSION}{w} | STATUS: {Fore.GREEN}● ONLINE{w} | DEV: {c}{AUTHOR}{b} <<< {c}║",
        f"{c}╚══════════════════════════════════════════════════════════════╝"
    ]
    for i in range(len(logo_lines)):
        clear_screen()
        for j in range(i + 1):
            print(logo_lines[j])
        time.sleep(0.05)
    time.sleep(0.3)
    # Показываем команды
    show_main_commands()

def filter_and_check(text):
    """Проверка на пустоту + фильтрация чужих имен"""
    if not text or str(text).strip() == "":
        return f"{Fore.RED}[ПЕРЕГРУЗКА ЯДРА]: Синхронизация нейронных связей нарушена. Повторите запрос."
    res = str(text)
    for word in FORBIDDEN_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        res = pattern.sub(AI_NAME, res)
    return res

def print_pro_output(text):
    """Профессиональный вывод текста с боковой гранью"""
    lines = text.split('\n')
    colors = [Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.LIGHTCYAN_EX]
    for line_idx, line in enumerate(lines):
        color = colors[line_idx % len(colors)]
        sys.stdout.write(f"{color}┃ {Fore.WHITE}")
        for char in line:
            if char in '.:!?':
                sys.stdout.write(f"{Fore.YELLOW}{char}{Fore.WHITE}")
            elif char.isdigit():
                sys.stdout.write(f"{Fore.CYAN}{char}{Fore.WHITE}")
            else:
                sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.008 if char != ' ' else 0.001)
        print()

def processing_animation():
    """Красивая анимация с синхронизацией"""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    messages = [
        "[SYNC] Установка нейронного соединения",
        "[PROC] Квантовая обработка запроса",
        "[ANAL] Анализ логических цепочек",
        "[GEN] Генерация оптимального ответа",
        "[VER] Верификация выходных данных"
    ]
    colors = [Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.LIGHTCYAN_EX, Fore.LIGHTMAGENTA_EX]
    start_time = time.time()
    i = 0
    while time.time() - start_time < 1.8:
        msg = messages[(i // 4) % len(messages)]
        color = colors[(i // 4) % len(colors)]
        sys.stdout.write(f"\r{color}{spinner[i % len(spinner)]} {Fore.WHITE}{msg} {color}{'.' * ((i % 3) + 1)} ")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * 80 + "\r")

def send_support_email(user_message, user_contact=""):
    """Отправка сообщения в поддержку"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = SUPPORT_EMAIL
        msg['Subject'] = f"SolverAI Support Request from {AUTHOR}"
        body = f"""
        ╔══════════════════════════════════════╗
        ║     SOLVER AI - SUPPORT REQUEST     ║
        ╠══════════════════════════════════════╣
        ║ Время: {time.strftime('%Y-%m-%d %H:%M:%S')}
        ║ Версия: {ENGINE} v{VERSION}
        ║ Пользователь: {AUTHOR}
        ║ Контакт: {user_contact if user_contact else 'Не указан'}
        ╠══════════════════════════════════════╣
        ║ СООБЩЕНИЕ:
        ║ {user_message}
        ╚══════════════════════════════════════╝
        """
        msg.attach(MIMEText(body, 'plain'))
        # Отправка в отдельном потоке
        def send():
            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
                server.quit()
            except:
                pass
        thread = threading.Thread(target=send)
        thread.daemon = True
        thread.start()
        return True
    except:
        return False

def support_menu():
    """Меню поддержки"""
    print(f"\n{cyber_border(70)}")
    print(f"{Fore.CYAN}╔{'═' * 68}╗")
    print(f"{Fore.CYAN}║{Fore.YELLOW}{'🆘 СЛУЖБА ПОДДЕРЖКИ SOLVER AI 🆘':^68}{Fore.CYAN}║")
    print(f"{Fore.CYAN}╠{'═' * 68}╣")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Пожалуйста, опишите вашу проблему или задайте вопрос.{' ' * 15}{Fore.CYAN}║")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Ваше сообщение будет отправлено на {Fore.CYAN}{SUPPORT_EMAIL}{' ' * 8}{Fore.CYAN}║")
    print(f"{Fore.CYAN}║ {Fore.WHITE}Для отмены введите {Fore.RED}'cancel'{Fore.WHITE} или {Fore.RED}'отмена'{' ' * 22}{Fore.CYAN}║")
    print(f"{Fore.CYAN}╚{'═' * 68}╝")
    print(f"{cyber_border(70)}\n")
    print(f"{Fore.CYAN}┌── {Fore.WHITE}[ ОПИШИТЕ ПРОБЛЕМУ ]")
    problem = input(f"{Fore.CYAN}└─{Fore.YELLOW}>> {Fore.WHITE}")
    if problem.lower() in ['cancel', 'отмена']:
        print(f"\n{Fore.YELLOW}[!] Отправка отменена.")
        return
    if not problem.strip():
        print(f"\n{Fore.RED}[!] Сообщение не может быть пустым.")
        return
    # Анимация отправки
    print(f"\n{Fore.CYAN}[SYNC] Отправка сообщения", end="")
    for _ in range(3):
        for dots in ['.', '..', '...']:
            sys.stdout.write(f"\r{Fore.CYAN}[SYNC] Отправка сообщения{dots} ")
            sys.stdout.flush()
            time.sleep(0.3)
    # Спрашиваем контакт
    print(f"\n{Fore.CYAN}┌── {Fore.WHITE}[ КОНТАКТ ДЛЯ ОТВЕТА ]")
    contact = input(f"{Fore.CYAN}└─{Fore.YELLOW}>> {Fore.WHITE}(Email/Telegram, или Enter чтобы пропустить): ")
    # Отправка
    if send_support_email(problem, contact):
        print(f"\n{Fore.GREEN}╔{'═' * 50}╗")
        print(f"{Fore.GREEN}║{Fore.WHITE}{'✅ СООБЩЕНИЕ УСПЕШНО ОТПРАВЛЕНО!':^50}{Fore.GREEN}║")
        print(f"{Fore.GREEN}║{Fore.WHITE}{'Мы ответим вам в ближайшее время.':^50}{Fore.GREEN}║")
        print(f"{Fore.GREEN}╚{'═' * 50}╝")
        play_success_sound()  # <-- ИСПОЛЬЗУЕМ НОВУЮ ФУНКЦИЮ
    else:
        print(f"\n{Fore.YELLOW}╔{'═' * 50}╗")
        print(f"{Fore.YELLOW}║{Fore.WHITE}{'⚠️ Не удалось отправить сообщение.':^50}{Fore.YELLOW}║")
        print(f"{Fore.YELLOW}║{Fore.WHITE}{f'Напишите нам напрямую: {SUPPORT_EMAIL}':^50}{Fore.YELLOW}║")
        print(f"{Fore.YELLOW}╚{'═' * 50}╝")

def show_help():
    """Показать все команды"""
    print(f"""
    {cyber_border(60)}
    {Fore.CYAN}╔{'═' * 58}╗
    {Fore.CYAN}║{Fore.YELLOW}{'📋 ВСЕ КОМАНДЫ':^58}{Fore.CYAN}║
    {Fore.CYAN}╠{'═' * 58}╣
    {Fore.CYAN}║ {Fore.GREEN}help{Fore.WHITE} - Показать все команды{' ' * 28}{Fore.CYAN}║
    {Fore.CYAN}║ {Fore.GREEN}clear{Fore.WHITE} - Очистить экран{' ' * 33}{Fore.CYAN}║
    {Fore.CYAN}║ {Fore.GREEN}support{Fore.WHITE} - Написать в поддержку{' ' * 26}{Fore.CYAN}║
    {Fore.CYAN}║ {Fore.GREEN}about{Fore.WHITE} - О программе{' ' * 33}{Fore.CYAN}║
    {Fore.CYAN}║ {Fore.GREEN}exit{Fore.WHITE} - Выйти из программы{' ' * 27}{Fore.CYAN}║
    {Fore.CYAN}║ {Fore.GREEN}выход{Fore.WHITE} - Выйти из программы{' ' * 27}{Fore.CYAN}║
    {Fore.CYAN}╚{'═' * 58}╝
    {cyber_border(60)}
    """)

def show_about():
    """О программе"""
    print(f"""
    {cyber_border(70)}
    {Fore.CYAN}╔{'═' * 68}╗
    {Fore.CYAN}║{Fore.YELLOW}{'ℹ️ О ПРОГРАММЕ':^68}{Fore.CYAN}║
    {Fore.CYAN}╠{'═' * 68}╣
    {Fore.CYAN}║ {Fore.WHITE}Название:{' ' * 10}{Fore.CYAN}{AI_NAME}{' ' * 41}{Fore.CYAN}║
    {Fore.CYAN}║ {Fore.WHITE}Версия:{' ' * 12}{Fore.MAGENTA}v{VERSION}{' ' * 43}{Fore.CYAN}║
    {Fore.CYAN}║ {Fore.WHITE}Ядро:{' ' * 14}{Fore.BLUE}{ENGINE}{' ' * 38}{Fore.CYAN}║
    {Fore.CYAN}║ {Fore.WHITE}Разработчик:{' ' * 7}{Fore.GREEN}{AUTHOR}{' ' * 37}{Fore.CYAN}║
    {Fore.CYAN}║ {Fore.WHITE}Поддержка:{' ' * 9}{Fore.CYAN}{SUPPORT_EMAIL}{' ' * 22}{Fore.CYAN}║
    {Fore.CYAN}║ {Fore.WHITE}Библиотека:{' ' * 8}{Fore.YELLOW}g4f (GPT4Free){' ' * 31}{Fore.CYAN}║
    {Fore.CYAN}╚{'═' * 68}╝
    {cyber_border(70)}
    """)

# === СТАРТ СИСТЕМЫ ===
animate_startup()
while True:
    try:
        print(f"\n{Fore.CYAN}┌── {Fore.WHITE}[ TERMINAL INPUT ]")
        user_input = input(f"{Fore.CYAN}└─{Fore.YELLOW}>> {Fore.WHITE}")
        if not user_input.strip():
            continue
        # Обработка команд
        cmd = user_input.lower().strip()
        if cmd in ['exit', 'выход']:
            print(f"\n{Fore.RED}╔══════════════════════════════╗")
            print(f"{Fore.RED}║   ОТКЛЮЧЕНИЕ ЯДРА SOLVER...  ║")
            print(f"{Fore.RED}╚══════════════════════════════╝")
            time.sleep(0.5)
            break
        elif cmd == 'help':
            show_help()
            continue
        elif cmd == 'clear':
            clear_screen()
            print(f"{Fore.GREEN}[✓] Экран очищен")
            continue
        elif cmd == 'support':
            support_menu()
            continue
        elif cmd == 'about':
            show_about()
            continue
        # Анимация синхронизации
        processing_animation()
        # Отправка запроса с блокировкой лишнего текста в консоль
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            raw_response = g4f.ChatCompletion.create(
                model=g4f.models.default,
                messages=[
                    {"role": "system", "content": SOLVER_IDENTITY},
                    {"role": "user", "content": f"{user_input} (Напоминание: ты {AI_NAME})"}
                ],
            )
            final_text = filter_and_check(raw_response)
        except Exception as api_error:
            final_text = f"{Fore.RED}[КРИТИЧЕСКАЯ ОШИБКА СИНХРОНИЗАЦИИ]: {api_error}"
        finally:
            sys.stdout = original_stdout
        
        play_system_sound()  # <-- ИСПОЛЬЗУЕМ НОВУЮ ФУНКЦИЮ
        
        # === КРАСИВЫЙ UI ВЫВОДА ===
        print(f"\n{cyber_border(70)}")
        print(f"{Fore.CYAN}╔{'═' * 68}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'◈ SOLVER ENGINE OUTPUT ◈':^68}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╠{'═' * 68}╣")
        print_pro_output(final_text)
        print(f"{Fore.CYAN}╚{'═' * 68}╝")
        print(f"{cyber_border(70)}")
        # Логирование
        with open("solver_v13.log", "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] Q: {user_input}\nA: {final_text}\n\n")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Принудительный сброс сессии.")
        break
    except Exception as e:
        if 'original_stdout' in locals(): sys.stdout = original_stdout
        print(f"\n{Fore.RED}[!] Сбой структуры: {e}")
        input(f"\n{Fore.CYAN}Сессия завершена. Нажмите Enter...")