from pydantic import ValidationError
from rest_framework.response import Response

from lib.api_view.base_api_view import BaseAPIView
from lib.responses.responses import BadResponse, NoContentResponse
from plagio.lib.engines import DuckDuckGoEngine, BraveSearchEngine
from plagio.models import Engines, SearchParamsRequest


class SearchView(BaseAPIView):
    def get(self, request):
        try:
            body = SearchParamsRequest(**request.data)

            available_engines = {
                Engines.DUCKDUCKGO: DuckDuckGoEngine(),
                Engines.BRAVE: BraveSearchEngine()
            }

            results = []
            similar_count = 0
            for engine in body.engines:
                engine_enum = engine if isinstance(engine, Engines) else Engines(engine)

                if engine_enum in available_engines:
                    engine_instance = available_engines[engine_enum]
                    engine_results, similarity = engine_instance.search(query=body.query,
                                                                       num_resultados=body.num_results)
                    results.extend(engine_results)
                    similar_count += similarity

            if similar_count == 0:
                return NoContentResponse({'query': body.query, 'similar_count': similar_count})

            results = sorted(results, key=lambda x: x['similarity_score'], reverse=True)
            response_data = {'query': body.query, 'search_results': len(results),'similar_count': similar_count, 'results': results}

            return Response(response_data)
        except ValidationError as e:
            return BadResponse({"errors": e.errors()})
