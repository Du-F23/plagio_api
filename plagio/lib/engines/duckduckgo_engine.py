import logging
from typing import List, Dict

from ddg import Duckduckgo

from plagio.lib.models.models import CommonResultsEngine
from plagio.lib.strategies.common_engine_strategy import CommonEngineStrategy

logger = logging.getLogger(__name__)


class DuckDuckGoEngine(CommonEngineStrategy):
    def __init__(self):
        self.engine = Duckduckgo()

    def search(self, query: str, num_resultados: int = 10) -> List[CommonResultsEngine]:
        try:
            logger.info(f'Searching for {query} on DuckDuckGo')
            search_results = self.engine.search(query=query).get('data')[:num_resultados]

            return DuckDuckGoEngine.format_result(search_results, query)
        except Exception as e:
            logger.error(f'Error searching for {query} on DuckDuckGo: {e}')
            return []
