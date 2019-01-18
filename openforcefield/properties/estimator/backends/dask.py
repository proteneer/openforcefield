# =============================================================================================
# MODULE DOCSTRING
# =============================================================================================

"""
Dask Property Estimator Backend

Authors
-------
* Simon Boothroyd <simon.boothroyd@choderalab.org>

"""


# =============================================================================================
# GLOBAL IMPORTS
# =============================================================================================

from dask import distributed

from openforcefield.properties.estimator.backends.base import PropertyEstimatorBackend


# =============================================================================================
# Base Backend Definition
# =============================================================================================

class DaskLocalClusterBackend(PropertyEstimatorBackend):
    """A property estimator backend which uses a dask `LocalCluster` to
    run calculations.
    """

    def __init__(self, number_of_workers=1, threads_per_worker=None):
        """Constructs a new DaskLocalClusterBackend"""
        super().__init__(number_of_workers, threads_per_worker)

        self._number_of_workers = number_of_workers
        self._threads_per_worker = threads_per_worker

        self._cluster = None
        self._client = None

    def start(self):

        self._cluster = distributed.LocalCluster(self._number_of_workers,
                                                 self._threads_per_worker,
                                                 processes=False)

        self._client = distributed.Client(self._cluster,
                                          processes=False)

    def stop(self):

        self._client.close()
        self._cluster.close()

    def submit_task(self, function, *args):
        return self._client.submit(function, *args)
