# Copyright 2019,2020,2021 Sony Corporation.
# Copyright 2021 Sony Group Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import nnabla.functions as F

from .utils import no_grad


def prelu_backward(grad_inputs, inputs, input_shapes, outputs, output_shapes, base_axis=1):
    """
    Args:
      grad_inputs (list of :obj:`nnabla.Variable`): Propagated grads to this backward function.
      inputs (list of :obj:`nnabla.Variable` and None): Input Variables of the forward function
          if this backward function depends on it. Otherwise, None is set instead.
      input_shapes (list of tuple of :obj:`int`): Input shapes of the forward function.
          The shapes of the inputs in which None is set can be passed.
      outputs (list of :obj:`nnabla.Variable` and None): Output Variables of the forward function
          if this backward function depends on it. Otherwise, None is set instead.
      output_shapes (list of tuple of :obj:`int`): Output shapes of the forward function.
          The shapes of the outputs in which None is set can be passed.
      kwargs (dict of arguments): Dictionary of the corresponding function arguments.

    Return:
      list of Variable: Return the gradients wrt inputs of the corresponding function.
    """
    dy = grad_inputs[0]
    x0 = inputs[0]
    w0 = inputs[1]

    base_axis += x0.ndim*(base_axis < 0)
    m0 = F.greater_scalar(x0, 0)
    m1 = 1 - m0
    m0 = no_grad(m0)
    m1 = no_grad(m1)
    if w0.shape == ():  # shared
        reshape = [1 for i in range(len(x0.shape))]
        w0 = F.reshape(w0, reshape, inplace=False)
        dw0 = F.sum(dy * x0 * m1)
    else:
        reshape = [w0.shape[0] if i ==
                   base_axis else 1 for i in range(len(x0.shape))]
        w0 = F.reshape(w0, reshape, inplace=False)
        raxes = [i for i in range(len(x0.shape)) if i != base_axis]
        dw0 = F.sum(dy * x0 * m1, raxes, keepdims=False)
    dx0 = dy * (m0 + w0 * m1)
    return dx0, dw0
