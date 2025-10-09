from rest_framework.response import Response

from lib.api_view.base_api_view import BaseAPIView
from lib.responses.responses import BadResponse
from plagio.lib.engines import DuckDuckGoEngine


class SearchView(BaseAPIView):
    def get(self, request):
        query = request.data.get('q', '')

        if not query or query.isspace():
            return BadResponse({'results': [], 'similar_count': 0,
                'query': 'Your search query is empty. Please provide a search query.'})
        duckduckgo = DuckDuckGoEngine()

        duckduckgo_results = duckduckgo.search(query=query)

        similar_count = len(duckduckgo_results)

        response_data = {'query': query, 'similar_count': similar_count, 'results': duckduckgo_results}

        return Response(response_data)
