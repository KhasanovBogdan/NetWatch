"""
NetWatch — прототип системы мониторинга сетевых ресурсов.

Программа проверяет доступность заданных сетевых узлов с помощью ping (ICMP)
и проверяет доступность указанных TCP-портов. Результаты каждой проверки
выводятся в консоль и сохраняются в CSV-журнал (monitoring_log.csv).

Автор: Мерданов Худайназар
"""

import csv
import platform
import socket
import subprocess
from datetime import datetime
from pathlib import Path


TARGETS = [
    {
        "name": "Google DNS",
        "host": "8.8.8.8",
        "ports": [53, 443]
    },
    {
        "name": "Cloudflare DNS",
        "host": "1.1.1.1",
        "ports": [53, 443]
    },
    {
        "name": "GitVerse",
        "host": "gitverse.ru",
        "ports": [80, 443]
    }
]

LOG_FILE = Path("monitoring_log.csv")


def ping_host(host: str) -> tuple[bool, str]:
    """Проверяет доступность узла с помощью системной утилиты ping."""
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", "2000", host]
    else:
        command = ["ping", "-c", "1", "-W", "2", host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )
        is_ok = result.returncode == 0
        return is_ok, "Доступен" if is_ok else "Недоступен"
    except subprocess.TimeoutExpired:
        return False, "Превышено время ожидания"
    except OSError as error:
        return False, f"Ошибка запуска ping: {error}"


def check_port(host: str, port: int, timeout: float = 2.0) -> tuple[bool, str]:
    """Проверяет доступность указанного TCP-порта на узле."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, "Открыт"
    except socket.timeout:
        return False, "Тайм-аут"
    except socket.gaierror:
        return False, "Ошибка DNS"
    except ConnectionRefusedError:
        return False, "Закрыт"
    except OSError:
        return False, "Недоступен"


def write_log(rows: list[dict]) -> None:
    """Дописывает результаты проверок в CSV-журнал."""
    file_exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "date_time",
                "target_name",
                "host",
                "check_type",
                "port",
                "status",
                "details"
            ]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerows(rows)


def monitor() -> None:
    """Основной сценарий: проверяет все цели и сохраняет результаты."""
    log_rows = []
    check_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 64)
    print("NetWatch — мониторинг сетевых ресурсов")
    print(f"Время запуска: {check_time}")
    print("=" * 64)

    for target in TARGETS:
        name = target["name"]
        host = target["host"]

        print(f"\nУзел: {name} ({host})")

        ping_status, ping_details = ping_host(host)
        ping_icon = "OK" if ping_status else "FAIL"
        print(f"  [{ping_icon}] Ping: {ping_details}")

        log_rows.append({
            "date_time": check_time,
            "target_name": name,
            "host": host,
            "check_type": "PING",
            "port": "-",
            "status": "OK" if ping_status else "FAIL",
            "details": ping_details
        })

        for port in target["ports"]:
            port_status, port_details = check_port(host, port)
            port_icon = "OK" if port_status else "FAIL"
            print(f"  [{port_icon}] TCP/{port}: {port_details}")

            log_rows.append({
                "date_time": check_time,
                "target_name": name,
                "host": host,
                "check_type": "TCP",
                "port": port,
                "status": "OK" if port_status else "FAIL",
                "details": port_details
            })

    write_log(log_rows)
    print("\nРезультаты сохранены в monitoring_log.csv")


if __name__ == "__main__":
    monitor()
