import logging

from abc import ABC, abstractmethod
from typing import List, Dict

from Levenshtein import ratio


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
    def search(self, query: str, num_resultados: int = 10)  -> List[Dict]:
        """
            This method is used to search with the help of search engines for the query that you receive through parameters
            :param query: string query to search
            :param num_resultados: int number of results to return
            :return: List[Dict]
        """
        pass

    @staticmethod
    def format_result(search_results: List, query: str) -> List[Dict]:
        similar_count = 0
        results = []
        logger.info(f'Found {len(search_results)} results')
        for r in search_results:
            similarity_score = CommonEngineStrategy.similarity(query, r.get('description'))
            if similarity_score >= 60:
                similar_count += 1
            results.append({'result': r, 'similarity_score': similarity_score})
        logger.info(f'{similar_count} results have a similarity score of at least 60%')
        results = sorted(results, key=lambda x: x['similarity_score'], reverse=True)
        logger.info(f'Sorted results by similarity score')
        return results