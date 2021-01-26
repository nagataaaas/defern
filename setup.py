"""
Provides Go-like `defer`
-----------
Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/delta114514/defern)

installation:
`$ pip install defern`

```python
from defern import defern, deferner, defern_this, here

def defer_multiple_function(frame):
    defern(lambda: print("it's middle 7th"), frame=frame)
    defern(lambda: print("it's middle 8th"), frame=frame)

print("Hi")

defern(lambda: print("it's middle 1st"))  # you can pass function to run after return.
defern(lambda: print("it's middle 2nd"))
defern(print, "it's middle 3rd")  # passed args and kwargs after function will given to function.

@deferner
def defer_this(number: str):
    print("it's middle", number)  # you can create function which runs after return with `@deferner`

defer_this("4th")
defer_this("5th", frame=here())

@defern_this  # wrap function to create procedure which automatically runs after return
def defer_this_now():
    print("it's middle 6th")

defer_multiple_function(here())  # here() to get currentFrame and pass it to `defern` or function created with `deferner`
                                 # with name `frame` will create `defern` to that frame

print('ended')

# Hi
# ended
# it's middle 1st
# it's middle 2nd
# it's middle 3rd
# it's middle 4th
# it's middle 5th
# it's middle 6th
# it's middle 7th
# it's middle 8th
```
"""

from setuptools import setup
from os import path

about = {}
with open("defern/__about__.py") as f:
    exec(f.read(), about)

here = path.abspath(path.dirname(__file__))

setup(name=about["__title__"],
      version=about["__version__"],
      url=about["__url__"],
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      description=about["__description__"],
      long_description=__doc__,
      long_description_content_type="text/markdown",
      packages=["defern"],
      zip_safe=False,
      platforms="any",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ])
