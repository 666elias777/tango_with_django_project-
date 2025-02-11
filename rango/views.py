from django.shortcuts import render, get_object_or_404
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

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
    pass

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    # Call the helper function to handle cookies BEFORE rendering the response
    visitor_cookie_handler(request)

    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list,
    }

    # Return response back to the user
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    """
    Renders the about page and displays the visit count.
    """
    # Ensure visitor cookies are processed
    visitor_cookie_handler(request)

    # Retrieve visit count from the session
    visits = request.session.get('visits', 1)

    context_dict = {
        'boldmessage': 'This tutorial has been put together with love!',
        'visits': visits  # Pass visit count to the template
    }

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
    pass


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()  
            registered = True 
        else:
            print(user_form.errors, profile_form.errors)
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                'rango/register.html',
                context = {'user_form': user_form,
                          'profile_form': profile_form,
                          'registered': registered})
                  
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return redirect(reverse('rango:index'))
        else:
            return HttpResponse("Invalid login details supplied.")
    
    return render(request, 'rango/login.html')

def login_view(request):
    return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                                'last_visit',
                                                str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                            '%Y-%m-%d %H:%M:%S')
        
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
        
    # Update/set the visits cookie
    request.session['visits'] = visits

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
        
