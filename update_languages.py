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
    if response.status_code != 200:
        print(f"Ошибка получения репозиториев: {response.status_code}")
        return []
    return response.json()

# Получаем статистику по языкам
def get_language_stats(repos):
    lang_stats = {}
    for repo in repos:
        if repo["private"] or not repo["fork"]:  # Собираем для приватных и не форкнутых репозиториев
            lang_url = repo["languages_url"]
            lang_data = requests.get(lang_url, headers=HEADERS).json()
            if lang_data:
                print(f"Languages for {repo['name']}: {lang_data}")  # Лог для отладки
                for lang, bytes in lang_data.items():
                    lang_stats[lang] = lang_stats.get(lang, 0) + bytes
    return lang_stats

# Генерация графика по языкам
def generate_language_chart(lang_stats):
    if not lang_stats:
        print("Нет данных по языкам для отображения")
        return

    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1], reverse=True)
    print(f"Sorted Languages: {sorted_langs}")  # Выводим отсортированный список для отладки
    if not sorted_langs:
        print("Нет популярных языков для отображения.")
        return

    langs, sizes = zip(*sorted_langs[:10])  # Берем 10 самых популярных языков

    plt.figure(figsize=(10, 6))
    plt.bar(langs, sizes)
    plt.xlabel("Языки программирования")
    plt.ylabel("Размер (байты)")
    plt.title(f"Топ 10 языков для пользователя {USERNAME}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Сохраняем график как изображение
    plt.savefig("language_chart.png")
    plt.close()
    print("График успешно сгенерирован и сохранен как 'language_chart.png'.")

# Основная логика
def main():
    # Получаем репозитории и статистику по языкам
    repos = get_repositories()
    if not repos:
        print("Не удалось получить репозитории. Завершаю выполнение.")
        return

    lang_stats = get_language_stats(repos)
    if not lang_stats:
        print("Не удалось получить статистику по языкам.")
        return

    # Генерируем график по языкам
    generate_language_chart(lang_stats)

    print("График успешно сгенерирован!")

if __name__ == "__main__":
    main()
