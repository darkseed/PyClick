
__author__ = 'Ilya Markov'


class SogouUtils:
    """
    Utility methods.
    """

    @staticmethod
    def get_retrieved_docs(search_sessions):
        """
        Extracts and returns the (query, retrieved_urls) from the sessions.

        :param search_sessions: The list of search sessions.
        :return: a dictionary. key is query, value is a set of urls retrieved for this query.
        """
        query2urls = {}
        for search_session in search_sessions:
            if search_session.query not in query2urls:
                query2urls[search_session.query] = set()
            for result in search_session.web_results:
                query2urls[search_session.query].add(result.id)
        return query2urls


