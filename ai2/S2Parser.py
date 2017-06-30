from pyclick.click_models.task_centric.TaskCentricSearchSession import TaskCentricSearchSession
from pyclick.search_session.SearchResult import SearchResult
import json

__author__ = 'Zhuyun Dai'


class S2Parser:
    """
    A parser for the sogou query log
    """

    @staticmethod
    def parse(sessions_filename, sessions_max=None):
        """
        Parses search sessions, formatted according to the Sogou query log.
        Returns a list of SearchSession objects.

        :param sessions_filename: The name of the file with search sessions formatted according to RPC.
        :param sessions_max: The maximum number of search sessions to return.
        If not set, all search sessions are parsed and returned.

        :returns: A list of parsed search sessions, wrapped into SearchSession objects.
        """
        sessions_file = open(sessions_filename, 'r')
        sessions = []

        session_id = 0
        for line in sessions_file:
            if 0 < sessions_max <= len(sessions):
                break

            obj = json.loads(line)

            query = obj['query']
            docs = obj['documents']
            for s in obj['sessions']:
                session_id += 1
                session = TaskCentricSearchSession(session_id, query)
                clicked_paper_ranks = set([int(o['index']) for o in s['clicks']])
                for doc in docs:
                    docid = doc['id']
                    rank = doc['position']
                    if_click = 0
                    if rank in clicked_paper_ranks:
                        if_click = 1
                    result = SearchResult(docid, if_click)
                    session.web_results.append(result)
                    if rank >= 10:
                        break  # only use the top10 results
                sessions.append(session)
            return sessions
