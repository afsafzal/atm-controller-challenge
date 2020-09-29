# The Controller for a Simple ATM

This project describes a simple ATM machine that
has the capabilities to connect to different bank
APIs, and performs authentication, account selection,
getting balance, deposit, and withdraw.

In this example, I made the assumption that there are
only $1 bills available, so all amounts are set to integer.
I also made the assumption that the banking API will take care
of authentication for any operations, and concurrency issues
(e.g., making sure it's not possible to withdraw/deposit from
two sources at the same time).

In real world, we should not store the session and user info
the way that is stored in this example, as it is very insecure.
We need to only store encrypted data for highly sensitive
information. In addition, in many of the functions I have used
simple integers as return type where each negative integer
represents failure in operation, and zero means success.
In real world, we may want to define specific return codes
for different failures.


### How to install and run

This project requires `Python 3.6` or later. You can create a
virtual environemnt using `pipenv`:
```
$ pipenv --python 3.8 shell
```

Then you can simply install the project using:
```
$ pip install .
```

The directory `test` includes all tests for the project that
can be executed using `pytest`:
```
$ pytest test
```
You can also check for the formating of the source code:
```
$ flake8 atm
```
And get the coverage of the tests:
```
$ coverage run --source=atm -m pytest test
$ coverage report -m
```


### Testing Travis
