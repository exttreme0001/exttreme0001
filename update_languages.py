import requests
import os

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

# Генерируем URL для генерации картинки с актуальной статистикой
def generate_image_url():
    image_url = f"https://github-readme-stats.vercel.app/api/top-langs?username={USERNAME}&show_icons=true&locale=en&layout=compact&count_private=true&token={GH_STATS_TOKEN}"
    return image_url

# Генерация Markdown кода для вставки в README.md
def generate_markdown_image(image_url):
    return f'<p><img align="left" src="{image_url}" alt="{USERNAME}" /></p>'

# Функция для обновления README.md
def update_readme(file_path, new_content):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Заменяем данные между маркерами
    start_marker = "<!-- LANGUAGES_START -->"
    end_marker = "<!-- LANGUAGES_END -->"
    new_content_block = f"{start_marker}\n{new_content}\n{end_marker}"

    updated_content = content.replace(f"{start_marker}\n(данные будут обновляться автоматически)\n{end_marker}", new_content_block)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

# Основная логика
def main():
    # Получаем репозитории и статистику по языкам
    repos = get_repositories()
    lang_stats = get_language_stats(repos)

    # Выводим статистику по языкам в лог
    print("Language statistics:")
    for lang, size in lang_stats.items():
        print(f"{lang}: {size / 1024:.2f} KB")

    # Генерируем URL для картинки
    image_url = generate_image_url()

    # Выводим URL картинки в лог
    print(f"Generated Image URL: {image_url}")

    # Генерируем Markdown код для вставки картинки в README
    readme_image_code = generate_markdown_image(image_url)

    # Обновляем README.md
    update_readme("README.md", readme_image_code)
    print("README.md успешно обновлен!")

if __name__ == "__main__":
    main()
