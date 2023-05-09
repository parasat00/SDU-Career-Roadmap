from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginatorLogic(request, queryset, elementsPerPage):
    page = request.GET.get('page')
    paginator = None
    paginator = Paginator(queryset, elementsPerPage)
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        page = 1
        queryset=paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        queryset = paginator.page(page)

    leftIndex = int(page) - 4
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = int(page) + 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages+1
    
    page_range = range(leftIndex, rightIndex)

    return queryset, page_range