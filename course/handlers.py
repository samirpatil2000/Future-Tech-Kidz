from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def paginator_object(objects, **kwargs):
    paginator = Paginator(objects, 5)  # creating a paginator object
    page_number = kwargs.get('page')

    try:
        page_obj = paginator.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj