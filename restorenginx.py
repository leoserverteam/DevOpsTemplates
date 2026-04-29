import os
import subprocess
import sys

def run_command(command):
    """Вспомогательная функция для запуска команд в shell."""
    try:
        # shell=True нужен для работы с подстановочными знаками типа *
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении: {e}")
        sys.exit(1)

def main():
    # Получаем переменные из окружения (environment variables)
    # Эти переменные должны быть прокинуты в workflow
    nginx_path = os.getenv("NGINX_PATH")
    backup_dir = os.getenv("BACKUP_DIR")

    if not nginx_path or not backup_dir:
        print("Ошибка: Переменные NGINX_PATH или BACKUP_DIR не заданы.")
        sys.exit(1)

    print(f"Очищаем папку: {nginx_path}")
    # Аналог rm -rf ${NGINX_PATH}/*
    run_command(f"rm -rf {nginx_path}/*")

    print(f"Восстанавливаем бэкап из: {backup_dir}")
    # Аналог cp -r ${BACKUP_DIR}/* ${NGINX_PATH}/
    run_command(f"cp -r {backup_dir}/* {nginx_path}/")

    print("Перезагружаем Nginx...")
    # Аналог sudo systemctl reload nginx
    run_command("sudo systemctl reload nginx")

    print("Восстановление успешно завершено.")

if __name__ == "__main__":
    main()
