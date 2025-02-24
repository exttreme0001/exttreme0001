def update_readme(file_path, new_content):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- LANGUAGES_START -->"
    end_marker = "<!-- LANGUAGES_END -->"

    # Проверяем, существуют ли маркеры
    if start_marker in content and end_marker in content:
        new_content_block = f"{start_marker}\n{new_content}\n{end_marker}"
        updated_content = content.replace(f"{start_marker}\n(данные будут обновляться автоматически)\n{end_marker}", new_content_block)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
    else:
        print(f"Маркер '{start_marker}' или '{end_marker}' не найден в файле {file_path}")
