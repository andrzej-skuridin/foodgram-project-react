from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from backend.foodgram.recipes.models import Recipe, Subscription, Favorite
from backend.foodgram.recipes.utils import paginator
from backend.foodgram.users.models import User


def index(request):
    """View-функция главной страницы"""
    recipes = Recipe.objects.all()
    context = dict(recipes=recipes, page_obj=paginator(request, recipes))
    return render(request, 'recipes/index.html', context)


def profile(request, username):
    """View-функция страницы пользователя"""
    recipes = get_object_or_404(Recipe, username=username).recipes_by_this_author.all()
    author = get_object_or_404(User, username=username)
    following = False
    if request.user.is_authenticated:
        following = Subscription.objects.filter(
            subscriber=request.user,
            author=get_object_or_404(User, username=username)
        ).exists()
    context = dict(recipes=recipes,
                   page_obj=paginator(request, recipes),
                   following=following,
                   posts_author=author)
    return render(request, 'users/profile.html', context)


def recipe_detail(request, recipe_id):
    """View-функция страницы отдельного рецепта"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_authenticated:
        # то есть возможность подписаться на этого автора
        pass
    context = dict(recipe=recipe)
    return render(request, 'users/post_detail.html', context)


@login_required
def subscriptions(request, username):
    """View-функция страницы, куда будут выведены рецепты авторов,
        на которых подписан текущий пользователь"""
    recipes = Recipe.objects.filter(author__following__user=request.user)
    context = dict(recipes=recipes)
    return render(request, 'users/follow.html', context)


@login_required
def profile_follow(request, username):
    """View-функция подписки на автора"""
    author = get_object_or_404(User, username=username)
    follow = Subscription.objects.filter(
        subscriber=request.user,
        author=author)
    # Если такой подписки нет, то создать её (на себя нельзя подписаться)
    if request.user != author and not follow.exists():
        Subscription.objects.create(
            subscriber=request.user,
            author=author
        )
    return redirect('users:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """View-функция отписки от автора"""
    Subscription.objects.filter(
        subscriber=request.user,
        author=get_object_or_404(User, username=username)
    ).delete()
    return redirect('users:profile', username=username)


@login_required
def add_to_favorites(request, recipe_id):
    """View-функция добавления в избранное"""
    favored_recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite = Favorite.objects.filter(
        user=request.user,
        recipe=favored_recipe
    )
    # Если рецепт уже не избран, то избрать его
    if not favorite.exists():
        Favorite.objects.create(
            user=request.user,
            recipe=favored_recipe
        )
    return redirect('users:profile', username=request.user)



@login_required
def remove_from_favorites(request, recipe_id):
    """View-функция удаления из избранного"""
    Favorite.objects.filter(
        user=request.user,
        recipe=get_object_or_404(Recipe, id=recipe_id)
    ).delete()
    return redirect('users:profile', request.user)


@login_required
def favorites_index(request):
    """View-функция страницы избранного"""
    # posts = Post.objects.filter(author__following__user=request.user)
    favorites = Recipe.objects.filter(is_followed_by=request.user)
    context = dict(favorites=favorites)
    return render(request, 'posts/follow.html', context)
