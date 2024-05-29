
# no_toplevel_code

Package to wrap a piece of python code in a function and function call, to avoid running code at the top level of a script.

## Example

E.g., if you have a script that looks like this:

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()
```

no_toplevel_code converts it to this:
    
```python
import numpy as np
import matplotlib.pyplot as plt

def _main():
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)

    plt.plot(x, y)
    plt.show()

_main()
```

## Interface

This package provides two functions: `wrap_code` and `unwrap_code` as well as their equivalent functions
    `wrap_ast` and `unwrap_ast`. The former functions take a string as input, while the latter functions
    take an AST (Abstract Syntax Tree) as input.
