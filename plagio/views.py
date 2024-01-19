from django.http import JsonResponse
#from duckduckgo_search import DDGS
from duckduckgo_search.errors import HTTPError 
from duckduckgo_search import DDGS
from fuzzywuzzy import fuzz


def similarity(a, b):
    return fuzz.partial_ratio(a, b)

def search_view(request):
    query = request.GET.get('q', '')  # Get the search term from the GET parameters

    results = []
    similar_count = 0

    try:
        with DDGS() as ddg:
            for r in ddg.text(query):
                similarity_score = similarity(query, r.get('body', ''))
                if similarity_score >= 60:
                    similar_count += 1
                results.append({'result': r, 'similarity_score': similarity_score})
    
    except HTTPError as e:
        # Handle HTTP errors from DuckDuckGo API
        error_message = f"HTTP Error from DuckDuckGo API: {e}"
        return JsonResponse({'error': error_message}, status=500)

     return JsonResponse(response_data, safe=False)
