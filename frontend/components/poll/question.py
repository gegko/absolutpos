import asyncio
import flet as ft

from network.requests import add_business, create_or_update_answer, update_business


class Question(ft.UserControl):
    def __init__(
        self,
        title: str,
        hint: str,
        question_id: str | None = None,
    ):
        super().__init__(col={"xs": 12, "sm": 12, "md": 10, "lg": 6, "xl": 6})
        self.title = title
        self.hint = hint
        self.question_id = question_id

    def collect_business_data(self, page: ft.Page):
        name = page.session.get("business_name")
        city = page.session.get("business_city")
        address = page.session.get("business_address")
        data = {
            "name": name,
            "city": city,
            "address": address,
        }
        return data

    def collect_question_data(self, page: ft.Page):
        business_id = page.session.get("business_id")
        question_id = self.question_id
        data = {
            "business_id": business_id,
            "question_id": question_id,
        }
        return data

    def save_new_business(self, page: ft.Page):
        data = self.collect_business_data(page=page)
        business_id = asyncio.run(add_business(data=data))["id"]
        page.session.set("business_id", business_id)

    def update_business_data(self, page: ft.Page):
        data = self.collect_business_data(page=page)
        business_id = page.session.get("business_id")
        asyncio.run(update_business(business_id=business_id, data=data))

    def change_dropdown_visibility(self, page: ft.Page):
        dropdown = page.views[-1].controls[0].controls[0].controls[-1]
        dropdown.visible = True
        dropdown.update()

    def final_touch(self, e: ft.ControlEvent):
        appbar = e.page.views[-1].appbar
        e.page.clean()
        e.page.appbar = appbar

        dlg = ft.AlertDialog(
            content=ft.Text("Спасибо! Мы Вам перезвоним!"),
            adaptive=True,
        )

        def open_dlg(e):
            e.page.dialog = dlg
            dlg.open = True
            e.page.update()

        open_dlg(e)
        # e.page.update()

    def save_answers(self, e: ft.ControlEvent):
        questions_answered = e.page.session.get("questions_answered")
        if not questions_answered:
            e.page.session.set("questions_answered", 1)
            e.control.data = 1
        else:
            if e.control.value:
                if not e.control.data:
                    questions_answered = e.page.session.get("questions_answered")
                    e.page.session.set("questions_answered", questions_answered + 1)
                    e.control.data = 1

                if self.title == "Название заведения":
                    e.page.session.set("business_name", e.control.value)
                elif self.title == "Страна и город":
                    e.page.session.set("business_city", e.control.value)
                elif self.title == "Адрес":
                    e.page.session.set("business_address", e.control.value)

            else:
                questions_answered = e.page.session.get("questions_answered")
                e.page.session.set("questions_answered", questions_answered - 1)
                e.control.data = 0

        questions_answered = e.page.session.get("questions_answered")
        if questions_answered == 3:
            self.change_dropdown_visibility(page=e.page)
            if not e.page.session.get("business_id"):
                self.save_new_business(page=e.page)
            else:
                self.update_business_data(page=e.page)

        if self.question_id:
            data = self.collect_question_data(page=e.page)
            data["text"] = e.control.value
            asyncio.run(create_or_update_answer(data=data))
        if to_answer := e.page.session.get("questions_to_answer"):
            if e.page.session.get("questions_answered") == to_answer + 3:
                controls = e.page.views[-1].controls[0].controls[0].controls
                if controls[-1].data != "finish":
                    finish = ft.Container(
                        content=ft.ElevatedButton(
                            "Завершить",
                            bgcolor=ft.colors.BLUE_500,
                            color=ft.colors.WHITE,
                            on_click=self.final_touch,
                        ),
                        margin=20,
                        alignment=ft.alignment.center,
                        data="finish",
                    )
                    controls.append(finish)
                    e.page.update()

    def build(self):
        return ft.Column(
            controls=[
                ft.Text(self.title, weight=ft.FontWeight.BOLD, size=12),
                ft.TextField(
                    hint_text=self.hint, border_radius=5, on_change=self.save_answers
                ),
            ],
            data=self.question_id,
            spacing=2,
        )


class PollGrid(ft.UserControl):
    def __init__(self, question_data: list[dict]):
        super().__init__()
        self.question_data = question_data

    def build(self):
        return ft.Container(
            margin=ft.Margin(0, 20, 0, 0),
            content=ft.Column(
                [
                    Question(
                        title=item["text"],
                        hint="Введите ответ",
                        question_id=item["id"],
                    )
                    for item in self.question_data
                ]
            ),
        )
