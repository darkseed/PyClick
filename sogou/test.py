import sys

from pyclick.click_models.Evaluation import LogLikelihood, Perplexity
from pyclick.utils.Utils import Utils
from pyclick.click_models.UBM import UBM
from pyclick.click_models.DBN import DBN
from pyclick.click_models.SDBN import SDBN
from pyclick.click_models.DCM import DCM
from pyclick.click_models.CCM import CCM
from pyclick.click_models.CTR import DCTR, RCTR, GCTR
from pyclick.click_models.CM import CM
from pyclick.click_models.PBM import PBM
from SogouParser import SogouParser

__author__ = 'Zhuyun Dai'


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "USAGE: %s <click_model> <dataset> <sessions_max>" % sys.argv[0]
        print "\tclick_model - the name of a click model to use."
        print "\tdataset - the path to the dataset from Yandex Relevance Prediction Challenge"
        print "\tsessions_max - the maximum number of one-query search sessions to consider"
        print ""
        sys.exit(1)

    click_model = globals()[sys.argv[1]]()
    search_sessions_path = sys.argv[2]
    search_sessions_num = int(sys.argv[3])

    search_sessions = SogouParser.parse(search_sessions_path, search_sessions_num)
    search_queries = Utils.get_unique_queries(search_sessions)


    print "-------------------------------"
    print "Training on %d search sessions (%d unique queries)." % (len(search_sessions), len(search_queries))
    print "-------------------------------"

    click_model.train(search_sessions)
    print "\tTrained %s click model:\n%r" % (click_model.__class__.__name__, click_model)

