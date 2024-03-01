import asyncio
import flet as ft

from network.requests import (
    add_question,
    delete_question,
    get_all_existing_business_areas,
    get_business_area_questions,
    get_question_areas,
    update_question,
)


class QuestionCard(ft.UserControl):
    def __init__(
        self,
        question_text: str | None = None,
        area_id: str | None = None,
        question_id: str | None = None,
    ):
        super().__init__()
        self.area_id = area_id
        self.question_id = question_id
        self.question_column = ft.Column(
            [
                ft.TextField(
                    value=question_text,
                    data=question_id,
                    prefix_icon=ft.icons.QUESTION_ANSWER,
                    shift_enter=True,
                    multiline=True,
                    border_color=ft.colors.GREY_400,
                    hint_text="Введите вопрос",
                    on_change=self.change_question,
                ),
                ft.TextButton(
                    text="Удалить",
                    icon=ft.icons.CLOSE,
                    icon_color=ft.colors.GREY_400,
                    style=ft.ButtonStyle(color=ft.colors.GREY_500),
                    height=40,
                    on_click=self.delete_question_card,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            col={"xs": 6, "sm": 6, "md": 5, "lg": 3, "xl": 3},
        )
        self.dropdowns = ft.Column(
            [
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("Red"),
                    ],
                    hint_text="Тип вопроса",
                    disabled=True,
                    border_color=ft.colors.GREY_200,
                    hint_style=ft.TextStyle(color=ft.colors.GREY_200),
                ),
                ft.ExpansionTile(
                    leading=ft.Icon(
                        ft.icons.HORIZONTAL_RULE_OUTLINED,
                        rotate=ft.Rotate(1.5708),
                        color=ft.colors.BLUE_500,
                    ),
                    title=ft.Text("Добавить к...", color=ft.colors.BLACK),
                    bgcolor=ft.colors.WHITE70,
                    controls=[
                        ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                        ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                    ],
                    initially_expanded=False,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=300,
            height=300,
            scroll=ft.ScrollMode.AUTO,
            col={"xs": 6, "sm": 6, "md": 5, "lg": 3, "xl": 3},
        )
        self.content = ft.Row(
            controls=[
                self.question_column,
                self.dropdowns,
            ],
            spacing=25,
            scroll=ft.ScrollMode.AUTO,
        )

    def change_question(self, e: ft.ControlEvent):
        if not e.control.data:
            text = e.control.value
            qid = asyncio.run(add_question(data={"text": text}))
            e.control.data = qid["id"]
        else:
            text = e.control.value
            business_areas = (
                self.controls[0].controls[0].content.controls[1].controls[1].controls
            )
            business_areas = [
                item.data for item in business_areas if item.leading.value
            ]

            asyncio.run(
                update_question(
                    question_id=e.control.data,
                    data={"text": text, "businessareas": business_areas},
                )
            )

    def change_question_checkbox(self, e: ft.ControlEvent):
        text_control = self.controls[0].controls[0].content.controls[0].controls[0]

        if not text_control.data:
            text = text_control.value
            if text:
                qid = asyncio.run(add_question(data={"text": text}))
                text_control.data = qid["id"]
        else:
            text = text_control.value
            business_areas = (
                self.controls[0].controls[0].content.controls[1].controls[1].controls
            )
            business_areas = [
                item.data for item in business_areas if item.leading.value
            ]

            asyncio.run(
                update_question(
                    question_id=text_control.data,
                    data={"text": text, "businessareas": business_areas},
                )
            )

    def fill_expansion_tile(self):
        data = asyncio.run(get_all_existing_business_areas())
        if self.question_id:
            areas = asyncio.run(get_question_areas(self.question_id))
            area_ids = {area["id"] for area in areas}
            return [
                ft.ListTile(
                    leading=ft.Checkbox(
                        value=item["id"] in area_ids,
                        on_change=self.change_question_checkbox,
                    ),
                    title=ft.Text(item["name"]),
                    data=item["id"],
                )
                for item in data
            ]
        return [
            ft.ListTile(
                leading=ft.Checkbox(
                    value=item["id"] == self.area_id,
                    on_change=self.change_question_checkbox,
                ),
                title=ft.Text(item["name"]),
                data=item["id"],
            )
            for item in data
        ]

    def delete_question_card(self, e: ft.ControlEvent):
        question_id = self.controls[0].controls[0].content.controls[0].controls[0].data
        if question_id:
            asyncio.run(delete_question(question_id))
        self.clean()

    def build(self):
        border_side = ft.BorderSide(1, color=ft.colors.GREY_400)
        self.dropdowns.controls[1].controls = self.fill_expansion_tile()
        return ft.ResponsiveRow(
            [
                ft.Container(
                    content=self.content,
                    border=ft.Border(
                        top=border_side,
                        bottom=border_side,
                        right=border_side,
                        left=ft.BorderSide(5, ft.colors.BLUE_500),
                    ),
                    col={"xs": 12, "sm": 12, "md": 10, "lg": 6, "xl": 6},
                    height=300,
                    padding=25,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )


class QuestionGrid(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.add_question_button = ft.IconButton(
            icon=ft.icons.ADD_CIRCLE_OUTLINE,
            icon_size=50,
            icon_color=ft.colors.BLUE_700,
            on_click=self.add_question_card,
        )
        self.selected_area_id = self.page.session.get("selected_area")
        self.questions = asyncio.run(get_business_area_questions(self.selected_area_id))

    def create_main_stack(self):
        return ft.Column(
            [
                QuestionCard(
                    area_id=self.selected_area_id,
                    question_text=item["text"],
                    question_id=item["id"],
                )
                for item in self.questions
            ]
        )

    def add_question_card(self, e: ft.ControlEvent):
        self.controls[0].controls.pop()
        self.controls[0].controls.append(QuestionCard(area_id=self.selected_area_id))
        self.controls[0].controls.append(self.add_question_button)
        self.update()

    def build(self):
        return ft.Column(
            controls=[
                self.create_main_stack(),
                self.add_question_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=self.page.width,
        )
