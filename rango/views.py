from django.shortcuts import render, get_object_or_404
from rango.models import Category, Page

def index(request):
    """
    Renders the homepage with the top 5 most liked categories and most viewed pages.
    """
    # Get top 5 categories by likes
    category_list = Category.objects.order_by('-likes')[:5]
    
    # Get top 5 pages by views
    page_list = Page.objects.order_by('-views')[:5]

    # Pass data to template
    context_dict = {
        'boldmessage': 'Hey there partner!',
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list
    }

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    """
    Renders the about page.
    """
    context_dict = {'boldmessage': 'This tutorial has been put together with love!'}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    """
    Displays a specific category and its associated pages.
    """
    # Context dictionary to store category and related pages
    context_dict = {}

    # Try to retrieve category by slug
    category = get_object_or_404(Category, slug=category_name_slug)

    # Get associated pages sorted by views
    pages = Page.objects.filter(category=category).order_by('-views')

    # Add category and pages to context
    context_dict['category'] = category
    context_dict['pages'] = pages

    return render(request, 'rango/category.html', context=context_dict)
