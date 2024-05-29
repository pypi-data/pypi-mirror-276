# Djecorator

Write Django routes in the same style as Flask.

## Installation

```
pip install djecorator
```

## Usage

### views.py

```python
from django.shortcuts import render
from djecorator import Route

route = Route()

@route("/")
def index(request):
    return render(request, "index.html")
```

### urls.py

```python
import views

urlpatterns = [
    ...
]

urlpatterns += views.route.patterns
```
