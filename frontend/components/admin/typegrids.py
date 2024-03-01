import asyncio
import flet as ft

from components.admin.questions import QuestionGrid
from network.requests import (
    add_business_area,
    delete_business_area,
    prefetch_business_area_data,
)


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
        self.type_grid: ft.Row = TypeGrid(
            self.prefetched_data,
            self.delete_func,
            self.prefetch_func,
            self.prefetch_id,
            level,
        )
        self.add_button = ft.IconButton(icon=ft.icons.ADD, on_click=self.show_to_add)
        self.hidden_to_add = ft.Row(
            controls=[
                ft.TextField(
                    width=150,
                    on_submit=self.add_to_grid,
                    autofocus=True,
                    **hints,
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
