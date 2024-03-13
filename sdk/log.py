import time

def append_log(filename: str, content: str):
    with open(f"log/{filename}.log", 'a', encoding='utf-8') as f:
        f.write(content + "\n")

formatted_log = lambda log_set, content: append_log(log_set, f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {content}")

module_log = lambda log_set, module, content: formatted_log(log_set, f"{module}: {content}")

logger = lambda log_set, module: {
    "info": lambda content: module_log(log_set, module, f"[INFO] {content}"),
    "warn": lambda content: module_log(log_set, module, f"[WARN] {content}"),
    "debug": lambda content: module_log(log_set, module, f"[DEBUG] {content}"),
    "error": lambda content: module_log(log_set, module, f"[ERROR] {content}")
}
