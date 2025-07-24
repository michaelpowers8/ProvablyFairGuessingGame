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

Given:
- Server Seed: `a1b2c3...` (64 hex chars)
- Client Seed: `x9y8z7...` (20 hex chars)
- Nonce: 5

Calculation Steps:
1. Create message: `":x9y8z7...:5:0"`
2. Generate HMAC-SHA256 using server seed as key
3. Take first 4 bytes of result: `[0x3A, 0x7F, 0xC1, 0x2B]`
4. Calculate:
   ```
   (58/256) + (127/65536) + (193/16777216) + (43/4294967296) = 0.22671998
   0.22671998 * 100 = 22.671998
   floor(22.671998) + 1 = 23
   ```
5. Final number: **23**

## Why This Is Fair

1. The house cannot predict or manipulate results because:
   - The server seed hash commits to a specific value
   - The client seed introduces player-controlled randomness
   - The nonce ensures every game is unique

2. Players can:
   - Verify all calculations post-game
   - Choose their own client seeds
   - Request new server seeds at any time
