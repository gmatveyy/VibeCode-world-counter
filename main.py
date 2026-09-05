import flet as ft

def main(page: ft.Page):
    page.title = "Счётчик слов"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 16
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Поле ввода текста
    text_input = ft.TextField(
        label="Текст для анализа",
        hint_text="Введите или вставьте текст...",
        multiline=True,
        min_lines=6,
        max_lines=14,
        border_radius=10,
    )

    # Виджеты вывода результатов
    words_counter = ft.Text("Слов: 0", size=22, weight=ft.FontWeight.BOLD)
    chars_counter = ft.Text("Символов: 0 (без пробелов: 0)", size=14, color=ft.Colors.GREY_600)
    lines_counter = ft.Text("Строк: 0", size=14, color=ft.Colors.GREY_600)

    # Функция расчёта статистики
    def update_stats(e=None):
        content = text_input.value or ""
        
        # split() автоматически делит строку по пробелам, табам и переносам
        words = len(content.split())
        total_chars = len(content)
        chars_no_spaces = len(content.replace(" ", "").replace("\n", "").replace("\t", ""))
        lines = len(content.splitlines()) if content else 0

        words_counter.value = f"Слов: {words}"
        chars_counter.value = f"Символов: {total_chars} (без пробелов: {chars_no_spaces})"
        lines_counter.value = f"Строк: {lines}"
        page.update()

    # Привязываем пересчёт к изменению содержимого в поле
    text_input.on_change = update_stats

    # Функция получения данных из системного буфера обмена
    def paste_from_clipboard(e):
        clipboard_text = page.get_clipboard()
        if clipboard_text:
            text_input.value = clipboard_text
            update_stats()
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Текст вставлен!"),
                duration=1200
            )
            page.snack_bar.open = True
            page.update()

    # Функция очистки поля
    def clear_text(e):
        text_input.value = ""
        update_stats()

    # Кнопки действий
    actions_row = ft.Row(
        controls=[
            ft.ElevatedButton(
                "Вставить",
                icon=ft.Icons.PASTE,
                on_click=paste_from_clipboard,
            ),
            ft.OutlinedButton(
                "Очистить",
                icon=ft.Icons.DELETE_OUTLINE,
                on_click=clear_text,
            ),
        ],
        spacing=10,
    )

    # Блок с отображением итоговой статистики
    stats_box = ft.Container(
        content=ft.Column(
            controls=[
                words_counter,
                chars_counter,
                lines_counter,
            ],
            spacing=4,
        ),
        padding=16,
        border_radius=12,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
    )

    # Размещение компонентов на странице
    page.add(
        actions_row,
        text_input,
        stats_box,
    )

if __name__ == "__main__":
    ft.app(target=main)