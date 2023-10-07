from django import template

from menu.services import get_menu_item_tree_by_slug, convert_tree_like_data_into_dict
from menu.utils import highlight_element
from tree_menu import settings

register = template.Library()


@register.simple_tag
def draw_menu(menu_slug: str) -> str:
    """ Функция формирует древовидный список экземпляра модели MenuItem """

    # получаем данные древовидного вида из бд в листе
    tree_result = get_menu_item_tree_by_slug(menu_slug)

    # форматируем полученные данные в удобный для работы вид
    menu_tree = convert_tree_like_data_into_dict(tree_result)

    # формируем словарь с главным родительским элементом, чтобы идти рекурсией вглубь и раскрывать его
    main_parent = dict()
    for value in menu_tree.values():
        if value["parent_id"] is None:
            main_parent = value

    def render_menu_item(menu_items: dict, is_child=False) -> str:
        """ Функция рекурсивно формирует строку html кода. """

        # если рассматриваемый menu item является выбранным в меню, мы выделяем его жирным шрифтом
        style = highlight_element(name=menu_items["slug"], slug=menu_slug)

        if not is_child:
            if menu_items['children'] is not None:
                return f'<li>' \
                       f'<a {style} href="{settings.DOMAIN_URL}/menu/{menu_items["slug"]}">{menu_items["name"]}</a>' \
                       f'<ul>{"".join(render_menu_item(child, is_child=True) for child in menu_items["children"])}</ul>' \
                       f'</li>'
            return f'<li>' \
                   f'<a {style} href="{settings.DOMAIN_URL}/menu/{menu_items["slug"]}">{menu_items["name"]}</a>' \
                   f'</li>'
        else:
            menu = menu_tree.get(menu_items['id'], None)
            if menu is not None:
                # рассматриваем переданный menu item как родителя в цепочке
                # от главного родителя, до выбранного menu item
                return render_menu_item(menu)
            else:
                # рассматриваем переданный menu item как элемент уровня родителя
                return f'<li>' \
                       f'<a {style} href="{settings.DOMAIN_URL}/menu/{menu_items["slug"]}">{menu_items["name"]}</a>' \
                       f'</li>'

    menu_html = "".join(render_menu_item(main_parent))  # формируются элементы списка
    data = f"<ul>{menu_html}</ul>"

    return data



