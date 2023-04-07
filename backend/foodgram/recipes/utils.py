from django.core.paginator import Paginator

from backend.foodgram.recipes.consts import RECIPES_PER_PAGE


def paginator(request, posts):
    paginator = Paginator(posts, RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
