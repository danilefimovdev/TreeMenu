from django.shortcuts import render


def get_menu(request, slug='main'):
    """ View отображает меню """

    # для начала нужно создать menu item с названием main для обработки menu/, либо переделать view
    # slug передается в контекст как имя меню, которое надо отобразить и выделить
    return render(request, 'start_page.html', context={'menu_slug': slug})
