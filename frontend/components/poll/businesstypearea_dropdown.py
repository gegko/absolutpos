import asyncio
import flet as ft

from components.poll.question import PollGrid
from network.requests import (
    get_business_area_questions,
    prefetch_business_area_data,
    prefetch_business_type_data,
    update_business,
)


class BusinessTypeAreaDropdown(ft.UserControl):

    def __init__(self, visible=False):
        super().__init__(
            col={"xs": 12, "sm": 12, "md": 10, "lg": 6, "xl": 6},
            visible=visible,
        )
        self.business_types = asyncio.run(prefetch_business_type_data())
        self.busines_type_options = [
            ft.dropdown.Option(text=business_type["name"], key=business_type["id"])
            for business_type in self.business_types
            if business_type["name"] != "DRAFT"
        ]
        self.busines_type_dropdown = ft.Dropdown(
            hint_text="Выберите сферу бизнеса",
            options=self.busines_type_options,
            on_change=self.business_type_change,
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
            on_change=self.business_area_change,
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
