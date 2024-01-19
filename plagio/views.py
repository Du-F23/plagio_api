from django.http import JsonResponse
#from duckduckgo_search import DDGS
from duckduckgo_search import DDGS
from fuzzywuzzy import fuzz


def similarity(a, b):
    return fuzz.partial_ratio(a, b)


def search_view(request):
    query = request.GET.get('q', '')  # Obtén el término de búsqueda de los parámetros GET

    results = []
    similar_count = 0

    with DDGS() as ddg:
        for r in ddg.text(query):
            similarity_score = similarity(query, r.get('body', ''))
            if similarity_score >= 60:  # Puedes ajustar este valor según tus necesidades
                similar_count += 1
            results.append({'result': r, 'similarity_score': similarity_score})

    response_data = {
        'results': results,
        'similar_count': similar_count
    }

    return JsonResponse(response_data, safe=False)
