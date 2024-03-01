import flet as ft
from components.admin.view import admin
from components.poll.view import poll



def main(page: ft.Page):
    page.padding = 20

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
        common_view_props = {
            "appbar": appbar,
            "scroll": ft.ScrollMode.AUTO,
            "auto_scroll": True,
        }
        if page.route == "/poll":
            page.session.clear()
            page.views.append(
                ft.View(route="/poll", controls=[poll()], **common_view_props)
            )
        else:
            page.views.append(
                ft.View(route="/", controls=[admin(page)], **common_view_props)
            )
        page.update()

    def view_pop(view: ft.View):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main, assets_dir="assets")
