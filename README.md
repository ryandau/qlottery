# 4-Game Quantum Lottery Generator

Generates 4 lottery entries (6 numbers from 1-45 each) using IBM quantum computers for true randomness.

## Quick Start

```bash
pip install qiskit-ibm-runtime
python quantum_4games.py
```

Enter IBM Quantum token on first run (get from [quantum.cloud.ibm.com](https://quantum.cloud.ibm.com)).

## Output

```
Game 1: [3, 12, 18, 25, 31, 44]
Game 2: [7, 14, 23, 29, 35, 42]  
Game 3: [5, 16, 21, 28, 33, 39]
Game 4: [9, 17, 24, 30, 36, 43]
```

## How It Works

1. Encodes all C(45,6) × 4 game combinations in 92-qubit superposition
2. Single quantum measurement collapses to one 4-game result
3. Decodes binary output to lottery numbers

* **Requirements**: 92 qubits (auto-selects available quantum computer)
* **Runtime**: 10-30 seconds per generation
* **Cost**: Free tier (10 min/month)

## Code Structure

```python
setup_ibm_quantum()              # Auth + connection
generate_4_game_combinations()   # Calculate combination space  
create_quantum_4_games()         # Main generation logic
```

## Technical Details

- **Combinations per game**: 8,145,060
- **Total quantum states**: 2^92 ≈ 4.95 × 10^27
- **Encoding**: 23 bits per game
- **Hardware**: ibm_brisbane (127+ qubits)

## Limitations

- Requires internet connection to IBM Quantum Platform
- Subject to quantum computer queue times
- Free tier usage limits apply

## License

MIT
