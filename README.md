# PyBitID

This is a python implementation of the BitID demo application originally developed in Ruby. 
Video demonstration (ruby): https://www.youtube.com/watch?v=3eepEWTnRTc
Live demo (ruby): http://bitid.bitcoin.blue/ 

The goal of this toy project is to illustrate how the BitId protocol works and how to implement it with helper functions provided by the PyBitId library.


## Python versions

Tested with Python 2.7.6 and 3.3.3


## Dependencies

Flask (http://flask.pocoo.org/) - A microframework for web development
```
pip install flask
```

PyBitId (https://github.com/LaurentMT/pybitid) - A python library for the BitId protocol
```
Gets the library from Github : https://github.com/LaurentMT/pybitid/archive/master.zip
Unzips the archive in root directory of the demo
Renames the "pybitid-master" directory in "pybitid"
```


## Todo

- Test authentication with an android smartphone
  You can get an android wallet supporting BitId at: https://github.com/bitid/bitcoin-wallet
  Before testing be sure that your server can be reached with an address different from localhost.


## Links
 - BitId protocol : https://github.com/bitid/bitid
 - PyBitId : https://github.com/LaurentMT/pybitid
 - Android wallet implementing BitId : https://github.com/bitid/bitcoin-wallet


## Author
Twitter: @LaurentMT


WORK IN PROGRESS !!! CONTRIBUTORS ARE WELCOME !

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
