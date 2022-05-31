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