# Analysis-of-Algorithim-Final-Project
A Python-based word guessing game using a Patricia Trie for fast word lookup. The game shows a prefix, and the user guesses a valid word. Built with Tkinter, it demonstrates efficient searching, basic trie concepts, and a simple interactive GUI with score tracking.

## Patricia Trie Word Game (Word Quest)

## Introduction

This project is a simple word guessing game built in Python. The game shows the first two letters of a word, and the player has to guess a correct English word starting with those letters.

To check answers quickly, the game uses a Patricia Trie, which helps search words very fast. This makes the game smooth and efficient even with many words.

## What is a Patricia Trie?

A Patricia Trie is a data structure used to store and search words efficiently.
It saves memory by combining common prefixes.

Example:
Words like cat, car, cap share “ca”, so it is stored once.

## Why This Algorithm?

Fast word searching
Works well with large dictionaries
Better than checking words one by one
Used in real applications like search and autocomplete

## How It Works

Words are loaded from words.txt
Stored inside a Patricia Trie
Game shows a 2-letter prefix
Player enters a word
Trie checks if the word exists
Score is updated

## Technologies Used

Python
Tkinter (GUI)
Data Structures (Trie)

## Features

Word guessing game
Fast answer checking
Score system
Simple GUI
Animated background

## Complexity

Search Time: O(1) to O(m)
Space: O(n × m)

## Real-World Use

Google search suggestions
Auto-complete
Spell checking
Dictionary apps

## Limitations

Uses more memory than lists
Only supports simple words
No autocomplete in this version

## Conclusion

This project shows how Patricia Trie can be used in real applications.
It makes searching fast and efficient and helps understand data structures in a practical way.
