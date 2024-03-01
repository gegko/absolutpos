import flet as ft
from components.poll.question import Question
from components.poll.businesstypearea_dropdown import BusinessTypeAreaDropdown


COLUMN_STYLE = {
    "col": {"xs": 12, "sm": 12, "md": 10, "lg": 6, "xl": 6},
    "spacing": 20,
}
QUESTION_1 = {
    "title": "Название заведения",
    "hint": "Введите название",
}
QUESTION_2 = {
    "title": "Страна и город",
    "hint": "Введите страну и город заведения",
}
QUESTION_3 = {
    "title": "Адрес",
    "hint": "Введите адрес",
}


def initial_questions_header(
        title: str = "Создайте первое заведение",
        postscriptum: str = "Вы всегда можете изменить данные в настройках"
) -> ft.ResponsiveRow:
    header_column = ft.Column(
        spacing=5,
        controls=[
            ft.Text(title, size=25, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Text(postscriptum, size=15),
                ft.Text("(но это не точно)", size=8),
            ]),
        ],
    )
    return ft.ResponsiveRow(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                col={"xs": 12, "sm": 12, "md": 10, "lg": 6, "xl": 6},
                content=header_column,
            )
        ],
    )


def poll() -> ft.ResponsiveRow:
    return ft.ResponsiveRow(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Column(
                controls=[
                    initial_questions_header(),
                    ft.Column(
                        controls=[
                            Question(**QUESTION_1),
                            Question(**QUESTION_2),
                            Question(**QUESTION_2),
                        ],
                        **COLUMN_STYLE,
                    ),
                    BusinessTypeAreaDropdown(),
                ],
                **COLUMN_STYLE,
            ),
        ],
    )
