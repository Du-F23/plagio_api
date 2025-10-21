import logging
from typing import List, Dict, Tuple

from brave import Brave
from django.conf import settings

from plagio.lib.models.models import CommonResultsEngine
from plagio.lib.strategies.common_engine_strategy import CommonEngineStrategy

logger = logging.getLogger(__name__)


class BraveSearchEngine(CommonEngineStrategy):
    def __init__(self):
        logger.info(f'Initializing BraveSearchEngine with Key: {settings.BRAVE_API_KEY}')
        self.engine = Brave(settings.BRAVE_API_KEY)

    def search(self, query: str, num_resultados: int = 10) -> List[Tuple[CommonResultsEngine, int]]:
        try:
            logger.info(f'Searching for {query} on Brave')
            query = query.replace("\n", " ").strip()

            search_results = self.engine.search(q=query[:400], count=num_resultados)

            return BraveSearchEngine.format_result(search_results.web_results, query)
        except Exception as e:
            logger.error(f'Error searching for {query} on Brave: {e}')
            return []