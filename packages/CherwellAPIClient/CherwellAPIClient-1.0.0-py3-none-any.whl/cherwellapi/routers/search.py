# -*- coding: utf-8 -*-

"""
Cherwell Search Router
"""

from cherwellapi.routers import CherwellRouter


class SearchRouter(CherwellRouter):
    """
    Class for interacting with Cherwell search functions
    """

    def __init__(self, url, headers, user, password, client_id, ssl_verify):
        super(SearchRouter, self).__init__(url, headers, user, password, client_id, ssl_verify)

    def get_search_results(self, search):
        """
        Get results of a Cherwell search

        Arguments:
            search (dict): A dictionary containing the search parameters to pass to cherwell

        Returns:
            list[dict]: List of dicts containing business object data
        """

        results = self._router_request(
            data=search,
            method='POST',
            api_version='api/V1',
            action='getsearchresults',
            response_timeout=30

        )

        search_results = {
            'total_rows': results['totalRows'],
            'returned_rows': len(results['businessObjects']),
            'data': results['businessObjects']
        }

        return search_results
