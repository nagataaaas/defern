"""
Provides Go-like `defer`
-----------
Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/nagataaaas/defern)

installation:
`$ pip install defern`

```python
from defern import defer, here

# note that defer is `last in first out`
def main():
    defer(print)('5th')
    defer(print)('4th')

    main_frame = here()

    def tmp():
        defer(print, main_frame)('3rd')
        # this will be called after the return of main()

        defer(print)('1st')
        # this will be called after the return of tmp()

    tmp()
    defer(print)('2nd')


defer(print)('6th')
main()

# output
# ------
# 1st
# 2nd
# 3rd
# 4th
# 5th
# 6th
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
