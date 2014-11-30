PlinPlin
========

PlinPlin is a Linda tuple space server with its access libraries, based on Redis and a python server. 


## Configuration ##

conf.ini contains all the possible configurations in the [global] area: 

* bind => ip address to listen to
* port => port to listen to

Then there are the optional infos. if you experience problems, you can change the dividers explicitly in the [dividers] area

* uuid_divider => "$#$"
* tuple_divider => "_|_"
* part_divider => ":::"

## Usage ##

Load a library in the language you need, connect to your IP and port, and start writing and reading (blocking and non-blocking, with remove and without).
