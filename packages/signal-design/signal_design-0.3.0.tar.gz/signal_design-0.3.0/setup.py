# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['signal_design']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3', 'typing_extensions>=4.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.8"': ['numpy<=1.19',
                                                         'scipy>=1.2,<1.8'],
 ':python_version >= "3.8"': ['numpy>1.19', 'scipy>=1.8']}

setup_kwargs = {
    'name': 'signal-design',
    'version': '0.3.0',
    'description': 'The project for creation and analysis signals.',
    'long_description': '# signal-design\n\nSimple way to create signals.\n\n## The project is intended for designing signals.\n\nThe package is intended to create and develop signals of\nvarying complexity.\n\nThe project can be used both for educational and work purposes.\n\nIt is convenient to use [`Jupyter Lab`](https://jupyter.org/) or\n[`Jupyter Notebook`](https://jupyter.org/) to speed up the development\nof signals, to compare their parameters with other signals,\nand to visualize them.\n\nThe project is designed so that you can easily change the creation of\nsignals.\n\nIn addition, documentation consist tutorial how to work with library\nand examples of ready-made signals. You can write own signal creation.\n\n# Installation\n\nTo install use:\n\n```bash\n$ pip install signal-design\n```\n\nor using `poetry`\n\n```bash\n$ poetry add signal-design\n```\n\nAlso you can clone or load project from [GitHub](https://github.com/Omnivanitate/signal-design),\nand install requirement packages using the\n\n```bash\n$ pip install -r requirements/build.txt\n```\n\nor if you want develop, use\n\n```bash\n$ pip install -r requirements/dev.txt\n\n```\n\nor\n\n```bash\n$ poetry install\n```\n\nor coping pieces of code and create your own.\n\n## Usage\n\nThe project is a library. Working with it is the same as with\nother third-part libraries of the python language.  \nAn example of how to include the library is described\n[here](https://docs.python.org/3/tutorial/modules.html).\n\nThe library consists sub-modules:\n\n- `signal_design.core` - contains basic classes `MathOperation` and `RelationProtocol`.\n- `signal_design.exc` - contains exceptions.\n- `signal_design.axis` - contains class `Axis`\n- `signal_design.relation` - contains class `Relation`\n- `signal_design.signal` - contains class `Signal`\n- `signal_design.spectrum` - contains class `Spectrum`\n- `signal_design.default_methods` - contains default methods for class above.\n\nFor convenient base classes:\n`Axis`, `Relation`, `Signal`, `Spectrum` - can be imported from\nthe `signal_design` module.\n\nFor example:\n\n```python\nfrom signal_design import Signal\n```\n\n### Quick start. Simple work flow.\n\nBelow is a simple example of creating a signal and visualizing it.\nA more extended description of the work of the library in the documentation.\nOther examples are contained in the documentation contains in _Tutorial_\nsection.\n\nFor the following code [`Matplotlib`](https://matplotlib.org/) need be used\nto visualize a result of work. But `Matplotlib` can be replaced with another\nlibrary that you use.\n\n```python\nimport numpy as np\nimport matplotlib.pyplot as plt\n\nfrom signal_design import Axis, Signal\n\ntime = Axis.get_using_end(start=0., end=10., sample=0.01)\namplitude = np.sin(2*np.pi*time.array)\nsignal = Signal(time, amplitude)\n\nplt.plot(*signal.get_data())\nplt.xlabel(\'Time, s\')\nplt.ylabel(\'Amplitude\')\nplt.title(\'Sin 1Hz\')\n```\n\nResult:\n\n![signal_with_matplotlib](https://raw.githubusercontent.com/Omnivanitate/signal-design/main/docs/assets/sin_func.png "Sin function.")\n\n## Credits\n\n`signal-design` was created with  \n[`numpy`](https://numpy.org/)  \n[`scipy`](https://scipy.org/)\n',
    'author': 'Omnivanitate',
    'author_email': 'serebraykov.vs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Omnivanitate/signal-design',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
