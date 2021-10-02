# anki-parser

**NOTE: I don't use this any more, and it isn't maintained.**

Contains some Python code that I use to automate my Anki deck learning

## Short explanation

Anki is a flashcard software. You put flashcards into it and it automatically schedules them for you at the rate you want to learn. It also calculates the best time to show you old cards so you don't forget them.

I use the anki-parser on two decks:

1. Vocab
2. Sentences

My learning workflow involves learning some words from the Vocab deck and then un-suspending (or unlocking) access to only the cards in the Sentences deck that contain vocab that I've learned. Doing this manually took up to 2 hours a day (if I chose to learn new vocab on that day).

The Python script will automate the process of searching the Anki cards database (using a much higher level of precision than is possible through the UI) and look for cards that I can 'unlock'. It will then use a SQL query to unlock all of the relevant cards at once, so I don't have to sit there and do it myself. This saves time, and lets me go through flashcards on autopilot, which allows me to learn a lot quicker.

## The files

- `main.py` - The main script. This must be run directly.
- `db-location.txt` - A text file which only has one line. That one line is the full filepath of my Anki card database.
- `databasehelper.py` - Contains a static python class with some helper methods for running database queries. Helps keep my `main.py` code clean.
- `textparser.py` - Contains a static python class with various helpful functions for parsing data, and handling lots of stuff in text format. Again, it's nice to put that parsing code in here to keep the main file clean.
