from django.core.paginator import Paginator


def paginate_and_add_to_context(
        queryset,
        context,
        model_name,
        per_page,
        request
):
    # Paginates a queryset and adds pagination details to context,
    # so they can be compatible with 'partials/pagination.html'.

    page_param = f'page_{model_name}s'
    page_number = request.GET.get(page_param, 1)

    paginator = Paginator(queryset, per_page)
    paginated_queryset = paginator.get_page(page_number)

    context[f'{model_name}s_paginated'] = paginated_queryset
    context[f'{model_name}s_page_param'] = page_param

    return context
