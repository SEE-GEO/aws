# Using QRNN to remove cloud impact in microwave channels

This repository contains code and documentation for a study that focusses on cloud correction of microwave humidity channels.


## Dependencies

For running ARTS simulations and retrieval, we are using the [parts](https://github.com/simonpf/parts) package.
It's is not available on PyPI yet, so you have to install it manually.

````
git clone https://github.com/simonpf/parts
cd parts
pip install -e
````

Note the `-e` flag for the `pip` command. This is allows the installed parts package to be updated, when
pulling a new version of parts.
 
QRNN is available as part of typhon package. 

https://github.com/atmtools/typhon.git


## Installation

To install the `aws` Python code simply run

````
pip install -e
````

in the root directory. Note also here the `-e` flag.

