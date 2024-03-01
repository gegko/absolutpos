import flet as ft
from components.admin.typegrids import GridControl
from network.requests import (
    prefetch_business_type_data,
    add_business_type,
    delete_business_type,
)



def admin(page: ft.Page):
    return GridControl(
        page=page,
        title="Сфера Бизнеса",
        hints={"label": "Тип бизнеса", "hint_text": "напр. Ритейл"},
        prefetch_func=prefetch_business_type_data,
        add_func=add_business_type,
        delete_func=delete_business_type,
    )
