from pyclick.click_models.task_centric.TaskCentricSearchSession import TaskCentricSearchSession
from pyclick.search_session.SearchResult import SearchResult
import codecs

__author__ = 'Zhuyun Dai'


class SogouParser:
    """
    A parser for the sogou query log
    """

    @staticmethod
    def parse(sessions_filename, sessions_max=None):
        """
        Parses search sessions, formatted according to the Sogou query log.
        Returns a list of SearchSession objects.

        format:
        UserID#session_ID#begin_time [url if_click(0 or 1) click_time vertical_flag] * T
        Seperated by \t

        :param sessions_filename: The name of the file with search sessions formatted according to RPC.
        :param sessions_max: The maximum number of search sessions to return.
        If not set, all search sessions are parsed and returned.

        :returns: A list of parsed search sessions, wrapped into SearchSession objects.
        """
        sessions_file = codecs.open(sessions_filename, 'r', 'gb2312')
        sessions = []

        for line in sessions_file:
            line = line.encode('utf-8')
            if sessions_max and len(sessions) >= sessions_max:
                break

            entry_array = line.strip().split("\t")

            if len(entry_array) % 4 != 2:  # format checking
                continue

            usr_id, session_id, begin_time = entry_array[0].split('#')
            query = entry_array[1].strip()
            session = TaskCentricSearchSession(session_id, query)
            i = 2

            while i < len(entry_array):
                url, if_click = entry_array[i: i + 2]
                i += 4
                result = SearchResult(url, int(if_click))
                session.web_results.append(result)
            sessions.append(session)
        return sessions
