import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
import os

# --- Настройки ---
API_URL = "https://api.github.com/search/users"
FAVORITES_FILE = "favorites.json"

# --- Загрузка избранных пользователей ---
def load_favorites():
    if not os.path.exists(FAVORITES_FILE):
        return []
    with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# --- Сохранение избранных пользователей ---
def save_favorites(favorites):
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)

# --- Поиск пользователей ---
def search_users():
    query = entry_search.get().strip()
    if not query:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
        return

    try:
        response = requests.get(API_URL, params={"q": query})
        response.raise_for_status()
        data = response.json()
        users = data.get("items", [])
        update_user_list(users)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")

# --- Обновление списка пользователей в GUI ---
def update_user_list(users):
    for widget in frame_users.winfo_children():
        widget.destroy()

    if not users:
        tk.Label(frame_users, text="Пользователи не найдены", fg="gray").pack(pady=10)
        return

    for user in users:
        user_frame = tk.Frame(frame_users, bg="#f0f0f0", bd=1, relief="groove")
        user_frame.pack(fill="x", padx=10, pady=5)

        name = user.get("login", "Без имени")
        avatar_url = user.get("avatar_url")
        html_url = user.get("html_url")

        # Загрузка аватара (опционально, требует Pillow)
        # Для простоты — только текст

        info_frame = tk.Frame(user_frame)
        info_frame.pack(side="left", padx=10)

        tk.Label(info_frame, text=name, font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(info_frame, text=html_url, font=("Arial", 9), fg="blue").pack(anchor="w")

        btn_fav = tk.Button(user_frame, text="Добавить в избранное",
                            command=lambda u=user: add_to_favorites(u))
        btn_fav.pack(side="right", padx=10)

# --- Добавление пользователя в избранное ---
def add_to_favorites(user):
    login = user.get("login")
    if not login:
        return

    favorites = load_favorites()
    if login not in favorites:
        favorites.append(login)
        save_favorites(favorites)
        messagebox.showinfo("Успех", f"Пользователь {login} добавлен в избранное!")
    else:
        messagebox.showinfo("Информация", f"Пользователь {login} уже в избранном.")

# --- Создание GUI ---
root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("600x500")
root.resizable(False, False)

# Поле поиска и кнопка
frame_search = tk.Frame(root)
frame_search.pack(pady=10, fill="x", padx=20)

entry_search = tk.Entry(frame_search, font=("Arial", 12), width=40)
entry_search.pack(side="left", expand=True, fill="x")

btn_search = tk.Button(frame_search, text="Поиск", command=search_users)
btn_search.pack(side="left", padx=5)

# Список пользователей
frame_users = tk.Frame(root, bg="#f9f9f9")
frame_users.pack(expand=True, fill="both", padx=20, pady=10)

# Запуск приложения
root.mainloop()
