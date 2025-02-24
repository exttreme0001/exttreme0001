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
                for lang, bytes in lang_data.items():
                    lang_stats[lang] = lang_stats.get(lang, 0) + bytes
    return lang_stats

# Генерация круговой диаграммы
def generate_pie_chart(lang_stats):
    if not lang_stats:
        print("Нет данных по языкам для отображения")
        return
    
    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1], reverse=True)
    langs, sizes = zip(*sorted_langs[:10])  # Берем 10 самых популярных языков
    total = sum(sizes)
    percentages = [size / total * 100 for size in sizes]

    plt.figure(figsize=(10, 6))
    plt.pie(percentages, labels=langs, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title(f"Топ 10 языков для пользователя {USERNAME}")
    plt.axis('equal')  # Сделать круг правильной формы
    plt.savefig("language_pie_chart.png")
    plt.close()
    print("График успешно сгенерирован: language_pie_chart.png")

# Основная логика
def main():
    repos = get_repositories()
    if not repos:
        print("Не удалось получить репозитории. Завершаю выполнение.")
        return

    lang_stats = get_language_stats(repos)
    if not lang_stats:
        print("Не удалось получить статистику по языкам.")
        return

    # Генерируем круговую диаграмму
    generate_pie_chart(lang_stats)

if __name__ == "__main__":
    main()
