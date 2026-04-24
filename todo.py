#!/usr/bin/env python3
"""Simple terminal To-Do app with JSON persistence."""

from __future__ import annotations

import json
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks() -> list[dict[str, object]]:
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return []


def save_tasks(tasks: list[dict[str, object]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def show_tasks(tasks: list[dict[str, object]]) -> None:
    if not tasks:
        print("\nBelum ada tugas.")
        return

    print("\nDaftar Tugas:")
    for idx, task in enumerate(tasks, start=1):
        status = "✅" if task.get("done") else "⬜"
        print(f"{idx}. {status} {task.get('title', '')}")


def add_task(tasks: list[dict[str, object]]) -> None:
    title = input("Masukkan judul tugas: ").strip()
    if not title:
        print("Judul tidak boleh kosong.")
        return
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print("Tugas berhasil ditambahkan.")


def mark_done(tasks: list[dict[str, object]]) -> None:
    show_tasks(tasks)
    if not tasks:
        return
    choice = input("Nomor tugas yang selesai: ").strip()
    if not choice.isdigit():
        print("Input harus angka.")
        return
    idx = int(choice) - 1
    if idx < 0 or idx >= len(tasks):
        print("Nomor tugas tidak valid.")
        return
    tasks[idx]["done"] = True
    save_tasks(tasks)
    print("Tugas ditandai selesai.")


def delete_task(tasks: list[dict[str, object]]) -> None:
    show_tasks(tasks)
    if not tasks:
        return
    choice = input("Nomor tugas yang ingin dihapus: ").strip()
    if not choice.isdigit():
        print("Input harus angka.")
        return
    idx = int(choice) - 1
    if idx < 0 or idx >= len(tasks):
        print("Nomor tugas tidak valid.")
        return
    removed = tasks.pop(idx)
    save_tasks(tasks)
    print(f"Tugas '{removed.get('title', '')}' dihapus.")


def main() -> None:
    tasks = load_tasks()

    while True:
        print("\n=== To-Do List Python ===")
        print("1. Lihat tugas")
        print("2. Tambah tugas")
        print("3. Tandai selesai")
        print("4. Hapus tugas")
        print("5. Keluar")

        menu = input("Pilih menu (1-5): ").strip()

        if menu == "1":
            show_tasks(tasks)
        elif menu == "2":
            add_task(tasks)
        elif menu == "3":
            mark_done(tasks)
        elif menu == "4":
            delete_task(tasks)
        elif menu == "5":
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()
