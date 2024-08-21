from django import template
from menu.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    menu_items = MenuItem.objects.filter(menu_name=menu_name).prefetch_related('children')
    current_path = request.path
    return render_menu(menu_items, current_path)


def render_menu(menu_items, current_path):
    html = '<ul>'
    for item in menu_items:
        active = 'active' if current_path == item.url else ''
        html += f'<li class="{active}"><a href="{item.url}">{item.title}</a>'
        if item.children.exists():
            html += render_menu(item.children.all(), current_path)
        html += '</li>'
    html += '</ul>'
    return html
