## Python Compute Module

Simple implementation of the Compute Module interface. Function definitions are automatically inferred using pydantic, allowing you to automatically register functions at runtime.

### Basic Usage

```python
from python_compute_module.app import ComputeModuleApp


app = ComputeModuleApp()


@app.function
def add(a: int, b: int) -> int:
    return a + b


@app.function
def multiply(a: int, b: int) -> int:
    return a * b


@app.function
def greet(a: str) -> int:
    return f"Greetings, {a}!"


if __name__ == '__main__':
    app.run()
```
