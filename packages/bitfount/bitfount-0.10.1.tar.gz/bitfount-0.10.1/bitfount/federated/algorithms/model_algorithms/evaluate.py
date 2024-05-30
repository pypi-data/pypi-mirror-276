"""Algorithm to evaluate a model on remote data."""

from __future__ import annotations

from typing import Any, Dict, Mapping, cast

import numpy as np

from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmFactory,
    _BaseModellerModelAlgorithm,
    _BaseWorkerModelAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.hub.api import BitfountHub
from bitfount.metrics import MetricCollection
from bitfount.types import _SerializedWeights
from bitfount.utils import delegates

logger = _get_federated_logger(__name__)


class _ModellerSide(_BaseModellerModelAlgorithm):
    """Modeller side of the ModelEvaluation algorithm."""

    def run(
        self, results: Mapping[str, Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        """Simply returns results."""
        return dict(results)


class _WorkerSide(_BaseWorkerModelAlgorithm):
    """Worker side of the ModelEvaluation algorithm."""

    def run(self, model_params: _SerializedWeights, **kwargs: Any) -> Dict[str, float]:
        """Runs evaluation and returns metrics."""
        self.update_params(model_params)
        preds, target = self.model.evaluate()
        # TODO: [BIT-1604] Remove these cast statements once they become superfluous.
        preds = cast(np.ndarray, preds)
        target = cast(np.ndarray, target)
        m = MetricCollection.create_from_model(self.model, self.model.metrics)
        return m.compute(target, preds)


@delegates()
class ModelEvaluation(_BaseModelAlgorithmFactory):
    """Algorithm for evaluating a model and returning metrics.

    :::note

    The metrics cannot currently be specified by the user.

    :::

    Args:
        model: The model to evaluate on remote data.

    Attributes:
        model: The model to evaluate on remote data.
    """

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the ModelEvaluation algorithm."""
        model = self._get_model_from_reference(project_id=self.project_id)
        return _ModellerSide(model=model, **kwargs)

    def worker(self, hub: BitfountHub, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the ModelEvaluation algorithm.

        Args:
            hub: `BitfountHub` object to use for communication with the hub.
        """
        model = self._get_model_from_reference(hub=hub, project_id=self.project_id)
        return _WorkerSide(model=model, **kwargs)
