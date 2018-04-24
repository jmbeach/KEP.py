KEP.py
=======

A Python parser of Kepware projects.


# Overview


KEP.py parses the .json files exportable from the KEPServerEX
Configuration client.

To use, read the contents of the .json file into a dictionary. Then,
create a `Project` object and pass it the dictionary.

From that project object, you can now get all of the channels of the
project and so on. The full list of the hierarchy you can reach is as
follows:

```
Channel
└─Device 
  ├─Register (See simulator device)
  └─Tag Group(s)
    ├─tag1
    ├─tag2
    ...
```

# Usage

Install with pip

`pip install keppy`

or clone and run

`python setup.py install`
