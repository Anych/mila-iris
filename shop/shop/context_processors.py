from category.models import Category


def menu_links(request):
    cloth_categories = Category.objects.get(slug='clothes').get_descendants(include_self=False)
    shoe_categories = Category.objects.get(slug='shoes').get_descendants(include_self=False)
    accessor_categories = Category.objects.get(slug='accessories').get_descendants(include_self=False)
    return dict(cloth_categories=cloth_categories, shoe_categories=shoe_categories,
                accessor_categories=accessor_categories)
