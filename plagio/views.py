from django.http import JsonResponse
from ddg import Duckduckgo
from fuzzywuzzy import fuzz
import json


def similarity(a, b):
    return fuzz.partial_ratio(a, b)


def duckduckgo_search(query):

    engine = Duckduckgo()

    try:
        search_results = engine.search(query).get('data')
        similar_count = 0
        results = []
        for r in search_results:
            similarity_score = similarity(query, r.get('description'))
            if similarity_score >= 60:
                similar_count += 1
            results.append({'result': r, 'similarity_score': similarity_score})

        return results

    except Exception as e:
        return JsonResponse({'error': str(e)})
        pass


def search_view(request):
    query = request.GET.get('q', '')

    if not query:
        return JsonResponse({
            'results': [],
            'similar_count': 0,
            'query': 'Your search query is empty. Please provide a search query.'
        }, safe=False)

    duckduckgo_results = duckduckgo_search(query)

    similar_count = len(duckduckgo_results)

    response_data = {
        'results': duckduckgo_results,
        'similar_count': similar_count,
        'query': query,
    }

    return JsonResponse(response_data, safe=False)
