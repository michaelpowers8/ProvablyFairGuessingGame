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

## How to install and run

1. Download python Windows Installer(64-bit) from [HERE](https://www.python.org/downloads/release/python-3126/) 
2. Open Command Prompt
3. cd C:\Path\To\Folder\Holding\ProvablyFairNumberGuessing.py
4. Type pip3 install -r requirements.txt
5. pythonw ProvablyFairNumberGuessing.py

## Provably Fair Calculation Breakdown

### Game Parameters
- **Server Seed**: 64-character hex string (generated randomly)
- **Client Seed**: 20-character hex string (player customizable to any number of characters)
- **Nonce**: Incrementing integer (starts at 1)
- **HMAC Algorithm**: HMAC-SHA256
- **Number Range**: 1-100

### Number Generation Process

#### Step 1: Seed Combination
The system combines seeds and nonce in this format:
{server seed}:{client seed}:{nonce}:{x}  # Where x is always 0 in this implementation

#### Step 2: HMAC-SHA256 Hashing
Creates HMAC using:
- Key: Server seed
- Message: Combined string from Step 1
- Algorithm: SHA256

```python
hmac_obj = hmac.new(server_seed.encode(), message.encode(), hashlib.sha256)
hex_result = hmac_obj.hexdigest()
```

#### Step 3: Hex to Bytes Conversion
Converts the HMAC result to bytes:
```python
bytes_list = list(bytes.fromhex(hex_result))
```

#### Step 4: Number Calculation
Uses first 4 bytes to generate the number:

```python
number = (
    (bytes_list[0]/256**1) +
    (bytes_list[1]/256**2) +
    (bytes_list[2]/256**3) +
    (bytes_list[3]/256**4)
) * 100
final_number = floor(number) + 1  # Result between 1-100
```

#### Verification Formula
To manually verify a game result:

1. Take these values from the game screen:
   - Server seed (hashed)
   - Client seed
   - Nonce

2. Recreate the HMAC:
   ```python
   message = f"{client_seed}:{nonce}:0"
   hmac_result = hmac.new(server_seed.encode(), message.encode(), hashlib.sha256).hexdigest()
   ```

3. Convert to bytes and calculate:
   ```python
   bytes_data = bytes.fromhex(hmac_result)
   calculated_number = floor((
       (bytes_data[0]/256**1) +
       (bytes_data[1]/256**2) +
       (bytes_data[2]/256**3) +
       (bytes_data[3]/256**4)
   ) * 100) + 1
   ```

### Fairness Guarantees

1. **Pre-commitment**: 
   - Server seed hash is shown before game starts
   - Actual server seed only revealed after rotation

2. **Transparency**:
   - All generation parameters visible
   - Deterministic algorithm ensures reproducibility

3. **Player Control**:
   - Client seed can be customized
   - Seeds can be rotated at any time

4. **Cryptographic Security**:
   - Uses industry-standard HMAC-SHA256
   - Secrets generated with cryptographically secure RNG (`secrets` module)

### Example Verification
```
Server Seed: aFDe1176F59bcCf9CaBf4d39D1D3dB36c2eeb04ccaEF1ca59Ea2DefcA4D5cABB 
Client Seed: EDD97dA3B4E83301aFba
Nonce: 1

Seeds to Hexadecimal Message:
HMAC_SHA256(aFDe1176F59bcCf9CaBf4d39D1D3dB36c2eeb04ccaEF1ca59Ea2DefcA4D5cABB:EDD97dA3B4E83301aFba:1:0)

Message to Hexadecimal:
5b, bd, d7, 79, 91, 19, 99, 93, 34, 4a, ab, bc, c8, 8f, f6, 6b, bc, c8, 81, 1b, b7, 7e, ed, d1, 14, 49, 99, 99, 9f, fd, d6, 69, 94, 4f, f6, 6b, ba, ad, d2, 28, 80, 0e, ea, a9, 9a, a0, 0e, e7, 71, 13, 3a, a8, 8e, e9, 9c, c8, 8e, ef, f8, 86, 6f, fa, a4, 4

Hexadecimal to Bytes:
91, 215, 145, 153, 52, 171, 200, 246, 188, 129, 183, 237, 20, 153, 159, 214, 148, 246, 186, 210, 128, 234, 154, 14, 113, 58, 142, 156, 142, 248, 111, 164


Bytes to Result Calculation:
  (91 / (256^1))
+ (215 / (256^2))
+ (145 / (256^3))
+ (153 / (256^4))
= 0.3687580679450184
=> 0.3687580679450184*100
=> 36.87580679450184 + 1 (So the minimum number is 1 not 0)
=> 37.87580679450184
=> 37
```
