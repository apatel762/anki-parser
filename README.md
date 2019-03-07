# anki-parser
Contains some Python code that I use to automate my Anki deck learning

There are two decks that I use:
* Vocab
* Sentences

My learning workflow involves learning some words from the Vocab deck and then un-suspending (or unlocking) access to only the cards in the Sentences deck that contain vocab that I've learned. Doing this manually took up to 2 hours a day (if I chose to learn new vocab on that day).

The Python script will automate the process of searching the Anki cards database (using a much higher level of precision than is possible through the UI) and look for cards that I can 'unlock'. It will then use a SQL query to unlock all of the relevant cards at once, so I don't have to sit there and do it myself.
