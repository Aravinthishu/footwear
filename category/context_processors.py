from .models import MainCategory

def categories(request):
    # Retrieve all MainCategory objects
    main_categories = MainCategory.objects.all()
    return {'main_categories': main_categories}
