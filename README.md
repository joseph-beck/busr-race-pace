# *`BUSR RACE PACE`*

Make graphs of race pace from a given CSV.

## *`Dependencies`*

- numpy
- curses
- matplotlib
- datetime
- csv
- scipy

## *`Usage`*

1. If you have not installed the dependencies use: \
`$ make install` or `$ pip install ...`

2. Run the app \
`$ make run` or `$ python3 main.py`

## *`Example CSV`*

```csv
DriverName, LapNumber,  Lap,        S1,     S2,     S3,     Tyres
driver,     1,          1:49.386,   37.159, 37.238, 34.988, Hard
driver,     1,          1:26.728,   29.112, 28.637, 28.978, Hard
```

## *`TODO:`*

- Add graph customisation options.
- More graph types.
- Add other session types like qualifying.
