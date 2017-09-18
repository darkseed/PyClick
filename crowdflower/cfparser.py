from pyclick.click_models.task_centric.TaskCentricSearchSession import TaskCentricSearchSession
from pyclick.search_session.SearchResult import SearchResult
import sys
import csv
reload(sys)
sys.setdefaultencoding('UTF8')


__author__ = 'Zhuyun Dai'


class CFParser:
    """
    A parser for the crowd flower click log
    """

    @staticmethod
    def parse(sessions_filename, sessions_max=None):
        """
        Parses search sessions, formatted according to the crowdlfower csv format.
        Returns a list of SearchSession objects.

        :param sessions_filename: The name of the file with search sessions formatted according to RPC.
        :param sessions_max: The maximum number of search sessions to return.
        If not set, all search sessions are parsed and returned.

        :returns: A list of parsed search sessions, wrapped into SearchSession objects.
        """
        sessions = []
        with open('names.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            session_id = 0
            for obj in reader:
                if sessions_max > 0 and sessions_max <= len(sessions):
                    break

                qid = obj['qid'].lower()
                session_id += 1
                session = TaskCentricSearchSession(session_id, qid)
                for rank in range(1, 21):
                    docid = obj['docno_{0}'.format(rank)]
                    if not docid:
                        continue
                    if_click = obj['click_{0}'.format(rank)]

                    if not if_click:
                        if_click = 0
                    else:
                        if_click = int(if_click)

                    result = SearchResult(docid, if_click)
                    session.web_results.append(result)

                sessions.append(session)
        return sessions
