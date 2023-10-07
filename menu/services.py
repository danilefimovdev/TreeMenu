from django.db import connection


def get_menu_item_tree_by_slug(menu_slug: str) -> list:
    """ Функция формирует древовидное структуру данных в виде листа, используя сырой sql запрос в бд """

    # возможно, я не совсем корректно понял ТЗ и поэтому решение для удовлетворения пункта 8 видел только в таком виде
    query = """
        WITH RECURSIVE menu_tree AS (
            SELECT id, name, slug, parent_id
            FROM menu_menuitem
            WHERE slug = %s
            UNION ALL
            SELECT mi.id, mi.name, mi.slug, mi.parent_id
            FROM menu_menuitem mi
            INNER JOIN menu_tree mt ON mi.id = mt.parent_id
        )
        SELECT mt.id, mt.name, mt.slug, mt.parent_id, json_agg(mt_child.*) FILTER (WHERE mt_child.id IS NOT NULL) AS children
        FROM menu_tree mt
        LEFT JOIN menu_menuitem mt_child ON mt.id = mt_child.parent_id
        GROUP BY mt.id, mt.name, mt.slug, mt.parent_id
        ORDER BY mt.id;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [menu_slug])
        result = cursor.fetchall()
    return result


def convert_tree_like_data_into_dict(tree_result: list) -> dict:

    menu_tree = {}

    for item_id, item_name, item_slug, parent_id, children_json in tree_result:
        menu_tree[item_id] = {
            'name': item_name,
            'slug': item_slug,
            'parent_id': parent_id,
            'children': children_json
        }
    return menu_tree
