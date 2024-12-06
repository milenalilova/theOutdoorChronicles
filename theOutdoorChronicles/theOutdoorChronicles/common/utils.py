from django.core.paginator import Paginator


def paginate_context(queryset, page_param, per_page, request):
    page_number = request.GET.get(page_param, 1)
    paginator = Paginator(queryset, per_page)

    return paginator.get_page(page_number)
