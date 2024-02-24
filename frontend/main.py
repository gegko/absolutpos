import aiohttp
import asyncio
import flet as ft

BASE_URL = "http://backend:8000/"


async def prefetch_business_type_data(*args) -> list[dict]:
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.get(f"/businesstype") as resp:
            response = await resp.json()
            return response


async def prefetch_business_area_data(*args) -> list[dict]:
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        business_type_id = args[0]
        async with session.get(f"/businessarea/{business_type_id}") as resp:
            response = await resp.json()
            return response


async def get_all_existing_business_areas(*args) -> list[dict]:
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.get("/businessarea") as resp:
            response = await resp.json()
            return response


async def add_business_type(*args, data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.post("/businesstype", json=data) as resp:
            print(resp.status)


async def add_business(data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.post("/business", json=data) as resp:
            response = await resp.json()
            return response


async def update_business(business_id: str, data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.patch(f"/business/{business_id}", json=data) as resp:
            print(resp.status)


async def add_business_area(*args, data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        business_type_id = args[0]
        data["businesstype_id"] = business_type_id
        async with session.post(f"/businessarea/{business_type_id}", json=data) as resp:
            print(resp.status)


async def delete_business_type(business_type_id: str):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.delete(f"/businesstype/{business_type_id}") as resp:
            print(resp.status)


async def delete_business_area(business_area_id: str):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.delete(f"/businessarea/{business_area_id}") as resp:
            print(resp.status)


async def delete_question(question_id: str):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.delete(f"/question/{question_id}") as resp:
            print(resp.status)


async def get_business_area_questions(business_area_id: str):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.get(f"/businessarea/{business_area_id}/questions") as resp:
            response = await resp.json()
            return response


async def get_question_areas(question_id: str):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.get(f"/question/{question_id}/business_areas") as resp:
            response = await resp.json()
            return response


async def add_question(*args, data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.post("/question", json=data) as resp:
            response = await resp.json()
            return response


async def update_question(*args, question_id: str, data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.patch(f"/question/{question_id}", json=data) as resp:
            print(resp.status)


async def create_or_update_answer(data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.post("/answer", json=data) as resp:
            print(resp.status)


class TypeGrid(ft.UserControl):

    def __init__(
        self,
        items: list[dict] | None,
        delete_func: callable,
        prefetch_func: callable,
        prefetch_id: str,
        level: int = 1,
    ):
        super().__init__()
        self.delete_func = delete_func
        self.prefetch_func = prefetch_func
        self.prefetch_id = prefetch_id
        self.style: dict = {
            "bgcolor": "#eff0fb",
            "padding": 25,
            "border_radius": 15,
            "shadow": ft.BoxShadow(
                blur_radius=1,
                offset=ft.Offset(1, 1),
                color=ft.colors.GREY_400,
            ),
        }
        self.items = items
        self.level = level

    def delete_item(self, e: ft.ControlEvent):
        type_id = e.control.data
        asyncio.run(self.delete_func(type_id))
        self.items = asyncio.run(self.prefetch_func(self.prefetch_id))
        self.controls[0] = self.build()
        self.update()

    def add_delete_func(self, e: ft.HoverEvent):
        if e.data == "true":
            e.control.content.controls[1].visible = True
            e.control.content.controls[0].opacity = 0.75
            e.control.content.controls[0].shadow = ft.BoxShadow(
                blur_radius=3,
                color=ft.colors.BLUE_100,
            )
            e.control.update()
        else:
            e.control.content.controls[1].visible = False
            e.control.content.controls[0].opacity = None
            e.control.content.controls[0].shadow = self.style["shadow"]
            e.control.update()

    def select_type(self, e: ft.ControlEvent):
        for control in self.controls[0].controls:
            control = control.content.controls[0]
            control.bgcolor = self.style["bgcolor"]
        self.controls[0].update()
        e.control.bgcolor = "#C6CAF1"
        e.control.update()
        if self.level == 1:
            e.page.session.set("selected_type", e.control.data)

            new_grid = GridControl(
                page=e.page,
                title="Направлениe",
                hints={"label": "Направлениe бизнеса", "hint_text": "напр. Ресторан"},
                prefetch_func=prefetch_business_area_data,
                add_func=add_business_area,
                delete_func=delete_business_area,
                level=2,
            )
            
            controls = e.page.views[-1].controls
            if len(controls) > 2:
                controls.pop()
                controls.pop()
            elif len(controls) > 1:
                controls.pop()
            controls.append(new_grid)
            e.page.update()

        else:
            e.page.session.set("selected_area", e.control.data)
            controls = e.page.views[-1].controls
            if len(controls) > 2:
                controls.pop()

            question_grid = QuestionGrid(page=e.page)
            controls.append(question_grid)
            e.page.update()

    def create_type_container(self, type_name: str, type_id: str):
        return ft.Container(
            ft.Stack(
                [
                    ft.Container(
                        content=ft.Text(
                            value=type_name,
                            color=ft.colors.BLACK54,
                            weight=ft.FontWeight.BOLD,
                        ),
                        data=type_id,
                        on_click=self.select_type,
                        **self.style,
                    ),
                    ft.IconButton(
                        icon=ft.icons.CLOSE,
                        icon_color=ft.colors.RED_500,
                        on_click=self.delete_item,
                        data=type_id,
                        top=0,
                        right=0,
                        visible=False,
                        icon_size=10,
                    ),
                ],
            ),
            on_hover=self.add_delete_func,
        )

    def build(self):
        if not self.items:
            return ft.Row()

        containers = [
            self.create_type_container(type_name["name"], type_name["id"])
            for type_name in self.items
        ]
        control = ft.Row(
            controls=containers,
            scroll=ft.ScrollMode.AUTO,
            auto_scroll=True,
        )
        return control


class GridControl(ft.UserControl):

    def __init__(
        self,
        page: ft.Page,
        title: str,
        hints: dict[str],
        prefetch_func: callable,
        add_func: callable,
        delete_func: callable,
        level: int = 1,
    ):
        super().__init__()
        self.page: ft.Page = page
        self.add_func = add_func
        self.delete_func = delete_func
        self.prefetch_func = prefetch_func
        self.prefetch_id = self.page.session.get("selected_type")
        self.prefetched_data: list[str] = asyncio.run(
            self.prefetch_func(self.prefetch_id)
        )
        self.title = ft.Text(value=title, width=150)
        self.type_grid: ft.Row = TypeGrid(self.prefetched_data, self.delete_func, self.prefetch_func, self.prefetch_id, level)
        self.add_button = ft.IconButton(icon=ft.icons.ADD, on_click=self.show_to_add)
        self.hidden_to_add = ft.Row(
            controls=[
                ft.TextField(
                    width=150,
                    on_submit=self.add_to_grid,
                    autofocus=True,
                    **hints
                    # label="Тип бизнеса",
                    # hint_text="напр. Ритейл",
                ),
                ft.ElevatedButton(text="Добавить", on_click=self.add_to_grid),
                ft.IconButton(icon=ft.icons.CLOSE, on_click=self.show_to_add),
            ]
        )

    def add_to_grid(self, e: ft.ControlEvent):
        try:
            data = e.control.value
            e.control.value = ""
        except AttributeError:
            data = self.controls[0].content.controls[-1].controls[0].value
            self.controls[0].content.controls[-1].controls[0].value = ""
        
        asyncio.run(self.add_func(self.prefetch_id, data={"name": data}))
        self.prefetched_data = asyncio.run(self.prefetch_func(self.prefetch_id))
        self.controls[0].content.controls[1] = TypeGrid(
            self.prefetched_data, self.delete_func, self.prefetch_func, self.prefetch_id
        )
        self.update()

    def delete_from_grid(self, e: ft.ControlEvent):
        type_id = e.control.data
        asyncio.run(self.delete_func(type_id))
        self.prefetched_data = asyncio.run(self.prefetch_func())
        self.controls[0].content.controls[1] = TypeGrid(
            self.prefetched_data, self.delete_func, self.prefetch_func, self.prefetch_id
        )
        self.update()

    def show_to_add(self, e: ft.ControlEvent):
        if len(self.controls[0].content.controls) < 4:
            self.controls[0].content.controls.append(self.hidden_to_add)
        else:
            self.controls[0].content.controls.pop()
        self.update()

    def build(self):
        return ft.SafeArea(
            ft.Row(
                controls=[self.title, self.type_grid, self.add_button],
                scroll=ft.ScrollMode.AUTO,
                auto_scroll=True,
            )
        )


class QuestionCard(ft.UserControl):
    def __init__(self, question_text: str | None = None, area_id: str | None = None, question_id: str | None = None):
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
        )
        self.content = ft.Row(
            controls=[
                self.question_column,
                self.dropdowns,
            ],
            spacing=25,
        )

    def change_question(self, e: ft.ControlEvent):
        if not e.control.data:
            text = e.control.value
            qid = asyncio.run(add_question(data={"text": text}))
            e.control.data = qid["id"]
        else:
            text = e.control.value
            business_areas = self.controls[0].controls[0].content.controls[1].controls[1].controls
            business_areas = [item.data for item in business_areas if item.leading.value]

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
            business_areas = self.controls[0].controls[0].content.controls[1].controls[1].controls
            business_areas = [item.data for item in business_areas if item.leading.value]

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
                        on_change=self.change_question_checkbox
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
                    col=6,
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
        return ft.Column([
            QuestionCard(
                area_id=self.selected_area_id,
                question_text=item["text"],
                question_id=item["id"],
            )
            for item in self.questions
        ])
    
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


def initial_questions_header():
    return ft.ResponsiveRow([
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Создайте первое заведение", size=25, weight=ft.FontWeight.BOLD), 
                    ft.Row([
                        ft.Text("Вы всегда можете изменить данные в настройках", size=15),
                        ft.Text("(но это не точно)", size=8),
                    ])
                ],
                spacing=5,
            ),
            col=6,
        )
    ], alignment=ft.MainAxisAlignment.CENTER)


class Question(ft.UserControl):
    def __init__(self, title: str, hint: str, question_id: str | None = None, col: int | None = None):
        super().__init__(col=6)
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
                ft.TextField(hint_text=self.hint, border_radius=5, on_change=self.save_answers),
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
            margin=ft.Margin(0,20,0,0),
            content=ft.Column([
                Question(title=item["text"], hint="Введите ответ", question_id=item["id"])
                for item in self.question_data
            ])
        )


class BusinessTypeAreaDropdown(ft.UserControl):

    def __init__(self, visible=False):
        super().__init__(col=6, visible=visible)
        self.business_types = asyncio.run(prefetch_business_type_data())
        self.busines_type_options = [
            ft.dropdown.Option(text=business_type["name"], key=business_type["id"])
            for business_type in self.business_types
            if business_type["name"] != "DRAFT"
        ]
        self.busines_type_dropdown = ft.Dropdown(
            hint_text="Выберите сферу бизнеса",
            options=self.busines_type_options,
            on_change=self.business_type_change
        )

    def get_business_areas(self, business_type_id: str):
        return asyncio.run(prefetch_business_area_data(business_type_id))

    def create_business_area_dropdown(self, business_type_id: str):
        areas = self.get_business_areas(business_type_id)
        options = [
            ft.dropdown.Option(text=business_area["name"], key=business_area["id"])
            for business_area in areas
            if business_area["name"] != "DRAFT"
        ]
        dropdown = ft.Dropdown(
            hint_text="Выберите направление бизнеса",
            options=options,
            on_change=self.business_area_change
        )
        return ft.Column(
            controls=[
                ft.Text("Направление бизнеса", weight=ft.FontWeight.BOLD, size=12),
                dropdown,
            ],
            spacing=2,
        )

    def collect_business_data(self, page: ft.Page):
        name = page.session.get("business_name")
        city = page.session.get("business_city")
        address = page.session.get("business_address")
        businesstype_id = page.session.get("business_type")
        businessarea_id = page.session.get("business_area")
        data = {
            "name": name,
            "city": city,
            "address": address,
            "businesstype_id": businesstype_id,
            "businessarea_id": businessarea_id,
        }
        return data

    def update_business_data(self, page: ft.Page):
        data = self.collect_business_data(page=page)
        business_id = page.session.get("business_id")
        asyncio.run(update_business(business_id=business_id, data=data))

    def business_type_change(self, e: ft.ControlEvent):
        e.page.session.set("business_type", e.control.value)
        self.update_business_data(e.page)
        new_area_dropdown = self.create_business_area_dropdown(e.control.value)
        if len(self.controls[0].controls) > 3:
            self.controls[0].controls.pop()
            self.controls[0].controls.pop()
        elif len(self.controls[0].controls) > 2:
            self.controls[0].controls.pop()
        self.controls[0].controls.append(new_area_dropdown)
        self.update()

    def business_area_change(self, e: ft.ControlEvent):
        e.page.session.set("business_area", e.control.value)
        self.update_business_data(e.page)
        new_area_questions = asyncio.run(get_business_area_questions(e.control.value))
        e.page.session.set("questions_to_answer", len(new_area_questions))
        if len(self.controls[0].controls) > 3:
            self.controls[0].controls.pop()
        self.controls[0].controls.append(PollGrid(new_area_questions))
        self.update()

    def build(self):

        return ft.Column(
            controls=[
                ft.Text("Сфера бизнеса", weight=ft.FontWeight.BOLD, size=12),
                self.busines_type_dropdown,
            ],
            spacing=2,
        )


def poll():
    return ft.ResponsiveRow(
        controls=[
            ft.Column(
                col=6,
                spacing=20,
                controls=[
                    initial_questions_header(),
                    ft.Column(
                        col=6,
                        controls=[
                            Question(
                                title="Название заведения", hint="Введите название"
                            ),
                            Question(
                                title="Страна и город",
                                hint="Введите страну и город заведения",
                            ),
                            Question(title="Адрес", hint="Введите адрес"),
                        ],
                        spacing=20,
                    ),
                    BusinessTypeAreaDropdown(),
                ],
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )


def main(page: ft.Page):
    page.padding = 20

    stack = GridControl(
        page=page,
        title="Сфера Бизнеса",
        hints={"label": "Тип бизнеса", "hint_text": "напр. Ритейл"},
        prefetch_func=prefetch_business_type_data,
        add_func=add_business_type,
        delete_func=delete_business_type,
    )

    def switch_routes(e: ft.ControlEvent):
        if e.page.route == "/":
            route = "/poll"
        else:
            route = "/"
        page.go(route=route)

    appbar = ft.AppBar(
        title=ft.Container(
            ft.Image(src="logo-apos.svg"),
            tooltip="Администрировать / Анкетировать",
            on_click=switch_routes,
        ),
        center_title=True,
    )

    def route_change(route: ft.RouteChangeEvent):
        page.views.clear()
        if page.route == "/poll":
            page.session.clear()
            page.views.append(
                ft.View(
                    route="/poll",
                    controls=[poll()],
                    appbar=appbar,
                    scroll=ft.ScrollMode.AUTO,
                    auto_scroll=True,
                )
            )
        else:
            page.views.append(
                ft.View(
                    route="/",
                    controls=[stack],
                    appbar=appbar,
                    scroll=ft.ScrollMode.AUTO,
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main, assets_dir="assets")
