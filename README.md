# Provably Fair Number Guessing Game

A secure, transparent number guessing game that uses cryptographic techniques to ensure fairness. Players guess a number between 1-100 with feedback on whether their guess is too high or too low.

## Features

- **Provably Fair System**: All game outcomes are verifiable using server seed, client seed, and nonce
- **Multiple Difficulty Levels**: 
  - Easy (6 guesses)
  - Medium (4 guesses)
  - Hard (2 guesses)
  - Expert (1 guess)
- **Seed Rotation**: Players can generate new server/client seeds
- **Transparent Verification**: All game parameters displayed on screen
- **Responsive UI**: Clean interface with visual feedback

## How It Works

The game uses:
- Server seed (generated randomly)
- Client seed (can be customized)
- Nonce (increments each game)
- HMAC-SHA256 for result generation

The number generation formula:
1. Combines seeds and nonce
2. Creates HMAC hash
3. Converts to number between 1-100

## Installation

1. Download python Windows Installer(64-bit) from [HERE](https://www.python.org/downloads/release/python-3126/) 
2. Open Command Prompt
3. Type pip3 install -r requirements.txt
4. pythonw
