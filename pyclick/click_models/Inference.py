#
# Copyright (C) 2015  Ilya Markov
#
# Full copyright notice can be found in LICENSE.
#
from abc import abstractmethod
import copy

__author__ = 'Ilya Markov'


class Inference(object):
    """An abstract inference algorithm for click models."""

    @abstractmethod
    def infer_params(self, click_model, search_sessions):
        """Infers parameters of the given click models based on the given list of search sessions."""
        pass


class MLEInference(Inference):
    """The maximum likelihood estimation (MLE) approach to parameter inference."""

    def infer_params(self, click_model, search_sessions):
        if search_sessions is None or len(search_sessions) == 0:
            return

        for search_session in search_sessions:
            session_params = click_model.get_session_params(search_session)

            for rank, result in enumerate(search_session.web_results):
                for param_name, param in list(session_params[rank].items()):
                    param.update(search_session, rank)


class EMInference(Inference):
    """The expectation-maximization (EM) approach to parameter inference."""

    ITERATION_NUM = 50
    """Number of iterations of the EM algorithm."""

    def __init__(self, iter_num=ITERATION_NUM):
        """
        Initializes the EM inference method with a given number of iterations.

        :param iter_num: The number of iterations to use.
        """
        self.iter_num = iter_num

    def infer_params(self, click_model, search_sessions):
        if search_sessions is None or len(search_sessions) == 0:
            return

        for iteration in range(self.iter_num):
            new_click_model = click_model.__class__()

            for search_session in search_sessions:
                current_session_params = click_model.get_session_params(search_session)
                new_session_params = new_click_model.get_session_params(search_session)

                for rank, result in enumerate(search_session.web_results):
                    for param_name, param in list(new_session_params[rank].items()):
                        param.update(search_session, rank, current_session_params)

            click_model.params = new_click_model.params
