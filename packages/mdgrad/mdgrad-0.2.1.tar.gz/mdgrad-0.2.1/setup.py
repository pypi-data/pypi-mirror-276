from setuptools import setup, find_packages
import os

VERSION = '0.2.1'
DESCRIPTION = 'Tensor-based autdiff engine and neural network API'
LONG_DESCRIPTION = """

# mdgrad

A small autograd engine that implements backpropagation (reverse-mode autodiff). Heavily inspired by karpathy's [micrograd](https://github.com/karpathy/micrograd/tree/master), and extended to support operations on tensors instead of scalars. Includes a small neural network api for building and training neural networks. Has a PyTorch-like API.

Hopefully useful as an educational resource.

## Installation

``` bash
pip install mdgrad
```

## Example Usage

A dumb example showing supported operations

```python

import mdgrad
import mdgrad.nn as nn

a = 3 * mdgrad.randn(3, 2)
b = mdgrad.ones(shape=(2, 2))
c = a @ b
d = c * 3 / 2
e = d ** 2
f = e.sum()
print(f.data) 
f.backward()
print(a.grad) 
```

An example showing how to define and run a neural network. See the files in `examples/` for more details on building and training models.

```python

import mdgrad
import mdgrad.nn as nn

# Define the model and loss function
model = nn.Sequential([
    nn.Linear(2, 20),
    nn.ReLU(),
    nn.Linear(20, 50), 
    nn.ReLU(),
    nn.Linear(50, 15),
    nn.ReLU(),
    nn.Linear(15, 1),
    nn.Sigmoid()
])
loss_fn = nn.MSELoss()

# Create dummy data
X = mdgrad.randn(100, 2)
target = mdgrad.randn(100, 1)

# Compute output and loss
out = model(X)
loss = loss_fn(out, target)

# Compute gradients of parameters
loss.backward()
```

                 """

# Setting up
setup(
    name="mdgrad",
    version=VERSION,
    author="Jordan Madden",
    author_email="<jordanmadden285@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'tensors', 'neural networks', 'automatic differentiation'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8'
)