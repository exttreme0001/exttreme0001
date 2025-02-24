import requests
import os
import matplotlib.pyplot as plt

# Получаем токен
GH_STATS_TOKEN = os.getenv("GH_STATS_TOKEN")
USERNAME = "exttreme0001"
HEADERS = {"Authorization": f"token {GH_STATS_TOKEN}"}

# Получаем список всех репозиториев
def get_repositories():
    url = f"https://api.github.com/user/repos?per_page=100&type=all"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

# Получаем статистику по языкам
def get_language_stats(repos):
    lang_stats = {}
    for repo in repos:
        if repo["private"] or not repo["fork"]:  # Собираем для приватных и не форкнутых репозиториев
            lang_url = repo["languages_url"]
            lang_data = requests.get(lang_url, headers=HEADERS).json()
            for lang, bytes in lang_data.items():
                lang_stats[lang] = lang_stats.get(lang, 0) + bytes
    return lang_stats

# Генерация графика с использованием Matplotlib
def generate_language_chart(lang_stats):
    # Сортируем по убыванию
    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1], reverse=True)
    langs, sizes = zip(*sorted_langs[:10])  # Берем 10 самых популярных языков

    # Создаем график
    plt.figure(figsize=(10, 6))
    plt.barh(langs, sizes, color='skyblue')
    plt.xlabel('Bytes')
    plt.title('Top 10 Languages by Bytes in Repositories')

    # Сохраняем изображение
    plt.tight_layout()
    plt.savefig("language_stats.png")
    plt.close()

# Основная логика
def main():
    # Получаем репозитории и статистику по языкам
    repos = get_repositories()
    lang_stats = get_language_stats(repos)

    # Генерируем график и сохраняем его как картинку
    generate_language_chart(lang_stats)

    print("language_stats.png успешно обновлен!")

if __name__ == "__main__":
    main()
