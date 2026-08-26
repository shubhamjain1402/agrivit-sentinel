"""Lightweight inference for the bundled legacy Keras pest classifier.

The production deployment intentionally avoids TensorFlow's large runtime. This
module reads the model's standard Conv2D/Dense weights from HDF5 and performs
the small 64x64 forward pass with NumPy.
"""

from __future__ import annotations

import h5py
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


class NumpyPestClassifier:
    """Inference-only implementation of the project's three-block CNN."""

    input_shape = (None, 64, 64, 3)

    def __init__(self, model_path: str):
        with h5py.File(model_path, "r") as model_file:
            weights = model_file["model_weights"]
            self.conv1 = self._layer_weights(weights, "conv2d_1")
            self.conv2 = self._layer_weights(weights, "conv2d_2")
            self.conv3 = self._layer_weights(weights, "conv2d_3")
            self.dense1 = self._layer_weights(weights, "dense_1")
            self.dense2 = self._layer_weights(weights, "dense_2")

        if self.dense2[1].shape != (10,):
            raise ValueError("The pest classifier must provide exactly 10 output classes")

    @staticmethod
    def _layer_weights(weights: h5py.Group, layer_name: str) -> tuple[np.ndarray, np.ndarray]:
        layer = weights[layer_name][layer_name]
        kernel = np.asarray(layer["kernel:0"], dtype=np.float32)
        bias = np.asarray(layer["bias:0"], dtype=np.float32)
        return kernel, bias

    @staticmethod
    def _conv_relu(inputs: np.ndarray, parameters: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
        kernel, bias = parameters
        kernel_height, kernel_width = kernel.shape[:2]
        windows = sliding_window_view(
            inputs,
            (kernel_height, kernel_width),
            axis=(1, 2),
        )
        windows = windows.transpose(0, 1, 2, 4, 5, 3)
        outputs = np.tensordot(windows, kernel, axes=([3, 4, 5], [0, 1, 2]))
        return np.maximum(outputs + bias, 0.0)

    @staticmethod
    def _max_pool(inputs: np.ndarray) -> np.ndarray:
        batch, height, width, channels = inputs.shape
        pooled_height = height // 2
        pooled_width = width // 2
        inputs = inputs[:, : pooled_height * 2, : pooled_width * 2, :]
        pooled = inputs.reshape(batch, pooled_height, 2, pooled_width, 2, channels)
        return pooled.max(axis=(2, 4))

    def predict(self, inputs: np.ndarray, verbose: int = 0) -> np.ndarray:
        del verbose
        values = np.asarray(inputs, dtype=np.float32)
        if values.ndim != 4 or values.shape[1:] != self.input_shape[1:]:
            raise ValueError(f"Expected input shaped (batch, 64, 64, 3); received {values.shape}")

        values = self._max_pool(self._conv_relu(values, self.conv1))
        values = self._max_pool(self._conv_relu(values, self.conv2))
        values = self._max_pool(self._conv_relu(values, self.conv3))
        values = values.reshape(values.shape[0], -1)

        dense1_kernel, dense1_bias = self.dense1
        values = np.maximum(values @ dense1_kernel + dense1_bias, 0.0)

        dense2_kernel, dense2_bias = self.dense2
        logits = values @ dense2_kernel + dense2_bias
        logits -= logits.max(axis=1, keepdims=True)
        probabilities = np.exp(logits)
        return probabilities / probabilities.sum(axis=1, keepdims=True)
