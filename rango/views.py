from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return redirect(reverse('rango:show_category', 
                                 kwargs={'category_name_slug': category.slug}))
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})

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

def add_category(request):
    form = CategoryForm()
    
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect(reverse('rango:index'))
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
            
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})
            
