import logging

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

from Levenshtein import ratio

from plagio.lib.models.models import CommonResultSearchEngine, CommonResultsEngine

logger = logging.getLogger(__name__)


class CommonEngineStrategy(ABC):
    @staticmethod
    def similarity(a: str, b: str):
        """
            This method is used to calculate the similarity between two strings
        :param a: string first string to compare
        :param b: string second string to compare
        :return:
        """
        similarity = ratio(a, b)
        similarity = round(similarity * 100, 2)

        return similarity

    @abstractmethod
    def search(self, query: str, num_resultados: int = 10)  -> List[CommonResultsEngine]:
        """
            This method is used to search with the help of search engines for the query that you receive through parameters
            :param query: string query to search
            :param num_resultados: int number of results to return
            :return: List[CommonResultsEngine]
        """
        pass

    @staticmethod
    def format_result(search_results: List, query: str) -> List[Tuple[CommonResultsEngine, int]]:
        similar_count = 0
        results = []
        logger.info(f'Found {len(search_results)} results')
        if len(search_results) != 0:
            for r in search_results:
                try:
                    similarity_score = CommonEngineStrategy.similarity(query, r.get('description'))
                    r['url'] = str(r.get('url'))
                    if similarity_score >= 60:
                        similar_count += 1
                    r = CommonResultSearchEngine(**r)

                    results.append(CommonResultsEngine(result=r, similarity_score=similarity_score).model_dump())
                except ValueError:
                    continue
            logger.info(f'{similar_count} results have a similarity score of at least 60%')
            results = sorted(results, key=lambda x: x['similarity_score'], reverse=True)
            logger.info(f'Sorted results by similarity score')

        return results, similar_count