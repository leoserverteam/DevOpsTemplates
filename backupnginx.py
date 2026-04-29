import os
import shutil
import sys


def run_backup():
    # Получаем переменные из окружения
    bak_path = os.getenv("BAK_PATH")
    src_path = os.getenv("SRC_PATH")

    # 1. Проверка: не пустой ли путь бэкапа (аналог if [ -z $BAK_PATH ])
    if not bak_path:
        print("❌ Error: backup_dir (BAK_PATH) is empty")
        sys.exit(1)

    try:
        # 2. Удаление старого бэкапа (аналог rm -rf $BAK_PATH)
        if os.path.exists(bak_path):
            shutil.rmtree(bak_path)

        # 3. Создание директории (аналог mkdir -p $BAK_PATH)
        os.makedirs(bak_path, exist_ok=True)

        # 4. Проверка источника (аналог if [ -d $SRC_PATH ] && [ "$(ls -A $SRC_PATH)" ])
        if src_path and os.path.isdir(src_path) and os.listdir(src_path):
            # Копируем содержимое (аналог cp -r $SRC_PATH/* $BAK_PATH)
            for item in os.listdir(src_path):
                s = os.path.join(src_path, item)
                d = os.path.join(bak_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

            print("✅ Backup done")
        else:
            print("⚠️ Source path is empty or not a directory")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_backup()
