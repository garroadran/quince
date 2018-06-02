# Contributing

The easiest way to contribute to the project is to add issues to the [issues page](https://github.com/garroadran/quince/issues) if you find something that needs to be improved or fixed. Any and all contributions are appreciated.

If you want to help out by contributing to the codebase, here's what you'll need in order to get set up.

### Requirements

- Python 3.6
- Pylint
- Git

## Getting Started

Starting from zero? If you're new to this sort of thing, here's what you'll need to do.

1. Fork the repository on GitHub (so that you get a copy of the repository under your own account)
2. Clone the repository to your working machine. This will usually be done by running the command `git clone https://github.com/your-user-name/quince.git`
3. It is recommended that you work inside of a virtual environment. If you don't know how to set one up on your machine, take a look at [this excellent article by Kenneth Reitz](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
4. Install all the necessary dependencies. You can do this by running `pip install -r requirements.txt`

Once all of this is done, you should be ready to start working on the code.

### What if I already did all that stuff but now the code on my computer is out of date?

If the codebase has moved on since the time you forked the project, you'll want to `pull` in the latest changes. There's a good explanation about how that works [here](https://git-scm.com/docs/git-pull), but the TL;DR is:

    # Add a remote to your Git project so that Git knows where the up-to-date code lives.
    $ git remote add upstream https://github.com/garroadran/quince

    # Update your local version of the code with the version that's on the upstream
    $ git pull upstream master

Life gets a little more complicated if the codebase has moved on while you are in the middle of making your own additions. You will need to merge in the latest changes, so that whatever files you change also contain whatever changes were made on the upstream. Read up on Git pulls and merges, and ask if you need assistance.

## Get To Work!

__When submitting a new feature or fix, be sure that you create a new branch for your work.__ Creating a new branch for your work can be done with the following command:

    $ git branch -b mynewbranch

Then write your changes and/or additions to the code as necessary. Wherever possible, please try to include tests with your additions.

## Before Pushing Your Code

Be sure to run all the unit tests, and that they all pass. This can be done from the root of the project directory by running `$ python -m unittest discover`.

You will also need to run `$ pylint quince/` and make sure that your code meets the style guide standards.

## Pushing Your Changes

Commit your changes, and then push your working branch to your fork of the repository.

    $ git push origin myworkingbranch

Then, from the GitHub website, you will have the option to Compare and send a Pull Request.

## Getting to know the code

Here is how you might play a game manually, using the python shell.

    $ python
    >>> import quince.components as components
    # Create a deck of cards, using the basic Card type (more card types may be added later)
    >>> deck = components.Deck(components.Card)
    # Create a couple of players
    >>> alice = components.Player('Alice')
    >>> bob = components.Player('Bob')
    # Deal 4 cards to the table, and 3 to each player
    >>> mesa = deck.deal(4)
    >>> alice.pick_up_hand(deck.deal(3))
    >>> bob.pick_up_hand(deck.deal(3))
    # Look at the cards on the table, and at Alice's cards
    >>> print(mesa)
    >>> [(2, 'oro'), (5, 'espada'), (5, 'copa'), (10, 'basto')]
    >>> print(alice.current_hand())
    >>> [(8, 'basto'), (10, 'espada'), (2, 'copa'), (1, 'basto')]
    # Alice can use her 10 to pick up one of the 5s
    >>> alice.pick_up_from_mesa(mesa, (10, 'espada'), [(5, 'copa')])
    # Look at the cards on the table, and at Bob's cards
    >>> print(mesa)
    >>> [(2, 'oro'), (5, 'espada'), (10, 'basto')]
    >>> print(bob.current_hand())
    >>> [(2, 'basto'), (2, 'espada'), (9, 'basto')]
    # Since bob can't pick up any cards, he has to lay a card down
    >>> bob.place_card_on_mesa((9, 'basto'))
