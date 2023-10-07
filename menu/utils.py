

def highlight_element(name: str, slug: str) -> str:
    """ Возвращает параметр style для выделения элемента выбранного меню """

    if name == slug:
        style = 'style="font-weight: bold;"'
    else:
        style = ''
    return style
