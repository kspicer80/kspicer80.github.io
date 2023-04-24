---
title: "Advanced Logging in Python"
date: 2023-04-27 00:01:00
draft: false
toc: false
tags:
  - python
  - python library
  - python standard library
  - python logging
  - code cleanup
  - codecademy projects
  - error messages
  - handling errors
---

Over this past weekend I was working my through [Codecademy's](https://www.codecademy.com/) "Advanced Python 3" [course](https://www.codecademy.com/learn/learn-advanced-python), which has an initial module that introduces students to Python's [```logging``` library](https://docs.python.org/3/library/logging.html). There was a wonderful little project—"ATM Logging"—that was quite fun to tackle, especially as it made really clear why one might want to use ```logging``` instead of filling one's code with a bunch of ```print()``` statements. The setup was that we had a pretty simple little "ATM" program/script that would allow us to deposit and withdraw money—while providing some error messages to keep track of things throughout the whole process. This is what my fiddling around here looked like.

So, the starter code given was the following:

```python
import random
import logging
import sys
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(level="INFO")

class BankAccount:
  def __init__(self):
    self.balance=100
    logger.logINFO("Hello! Welcome to the ATM Depot!")

  def authenticate(self):
    while True:
      pin = int(input("Enter account pin: "))
      if pin != 1234:
        print("Error! Invalid pin. Try again.")
      else:
        return None

  def deposit(self):
    try:
      amount=float(input("Enter amount to be deposited: "))
      if amount < 0:
        print("Warning! You entered a negative number to deposit.")
      self.balance += amount
      print("Amount Deposited: ${amount}".format(amount=amount))
      print("Transaction Info:")
      print("Status: Successful")
      print("Transaction #{number}".format(number=random.randint(10000, 1000000)))
      print("Timestamp: {timestamp}".format(timestamp=datetime.now()))
    except ValueError:
      print("Error! You entered a non-number value to deposit.")
      print("Transaction Info:")
      print("Status: Failed")
      print("Transaction #{number}".format(number=random.randint(10000, 1000000)))
      print("Timestamp: {timestamp}".format(timestamp=datetime.now()))

  def withdraw(self):
    try:
      amount = float(input("Enter amount to be withdrawn: "))
      if self.balance >= amount:
        self.balance -= amount
        print("You withdrew: ${amount}".format( amount=amount))
        print("Transaction Info:")
        print("Status: Successful")
        print("Transaction #{number}".format(number=random.randint(10000, 1000000)))
      else:
        print("Error! Insufficient balance to complete withdraw.")
        print("Transaction Info:")
        print("Status: Failed")
        print("Transaction #{number}".format(number=random.randint(10000, 1000000)))
    except ValueError:
      print("Error! You entered a non-number value to withdraw.")
      print("Transaction Info:")
      print("Status: Failed")
      print("Transaction #{number}".format(number=random.randint(10000, 1000000)))
      print("Timestamp: {timestamp}".format(timestamp=datetime.now()))

  def display(self):
    print("Available Balance = ${balance}".format(balance=self.balance))

acct = BankAccount()
acct.authenticate()
acct.deposit()
acct.withdraw()
acct.display()
```

The task was to see if we could clean things up a little bit here—paring down some of the code (the original had 68 lines), remove extraneous print statements, etc. Just from glancing casually at the code, it might be clear why we would want to do such things. From the point of view of the ```logging``` library, there's much to do here that can be handled in far fewer lines of code. If we utilize all the affordances of the library, we can get something that is much more streamlined and efficient and perhaps much more helpful for users.

```python
import random
import logging
import sys
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Adding stream handler to logger
stream_handler = logging.StreamHandler(sys.stdout)
formatter1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter1)
logger.addHandler(stream_handler)

# Adding File handler to logger
file_handler = logging.FileHandler("log_test.txt")
formatter2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter2)
logger.addHandler(file_handler)

class BankAccount:
    def __init__(self):
        self.balance=100
        logger.info("Hello! Welcome to the ATM Depot!")

    def authenticate(self):
        while True:
            pin = int(input("Enter account pin: "))
            if pin != 1234:
                logger.error("Error! Invalid pin. Try again.")
            else:
                return None

    def deposit(self):
        try:
            amount=float(input("Enter amount to be deposited: "))
            if amount < 0:
                logger.warning("Warning! You entered a negative number to deposit.")
            else:
                self.balance += amount
                logger.info("You deposited ${amount: .2f} at {timestamp} and your Transation # is {number}".format(amount=amount, timestamp=datetime.now(), number=random.randint(1, 10)))
        except ValueError:
            logger.error("Error! You entered a non-number value to deposit!")

    def withdraw(self):
        try:
            amount = float(input("Enter amount to be withdrawn: "))
            if self.balance >= amount:
                self.balance -= amount
                logger.info("You withdrew {amount: .2f} at {timestamp}; your Transation # is {number}.".format(amount=amount, timestamp=datetime.now(), number=random.randint(1, 10)))
            else:
                logger.error("Error! Insufficient balance to complete withdraw.")
        except ValueError:
            logger.error("Error! You entered a non-number value to withdraw.")

    def display(self):
        logger.info("Available Balance = ${balance: .2f}.".format(balance=self.balance))

acct = BankAccount()
acct.authenticate()
acct.deposit()
acct.withdraw()
acct.display()
```

The cleaned-up version doesn't really get us fewer lines of code, but it does look much, much more readable and far easier to understand. And the error messages are successfully logged to the proper places, which is the whole point of this, to be sure! Output where we don't get any error messages looks like this now:

![output_with_no_errors](/images/imgforblogposts/post_33/output_of_reworked_script.png)

Here's the output if a user incorrectly/inadvertently enters a negative number:

![negative_value_output_error](/images/imgforblogposts/post_33/negative_value_entered.png)

and if they try to withdraw more funds than they have in their current balance:

![insufficient_balance_output_error](/images/imgforblogposts/post_33/insufficient_balance_log.png)

This was quite fun and I learned a ton: it's exceedingly clear to me how useful this ```logging``` module is, that's for sure.


All the work for this project is available in the following [repository](https://github.com/kspicer80/codecademy_work/tree/main/advanced_python_course).