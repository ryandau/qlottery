# Quantum Multi-Game Lottery Generator

A practical demonstration of quantum computing principles using IBM Quantum hardware to generate lottery number combinations through quantum superposition and measurement.

## Overview

This project leverages quantum superposition to generate multiple lottery games simultaneously from a single quantum measurement. The implementation demonstrates quantum state collapse and provides truly random number generation using real quantum hardware.

## Features

- **Quantum Superposition**: Creates a superposition of all possible game combinations
- **Simultaneous Generation**: Produces multiple lottery games from a single quantum measurement
- **IBM Quantum Integration**: Executes on real quantum hardware via IBM Quantum Cloud
- **Configurable Parameters**: Customizable number range, games per ticket, and numbers per game
- **Production-Ready**: Clean architecture with proper error handling and logging

## Technical Details

### Quantum Algorithm

1. **State Preparation**: Applies Hadamard gates to all qubits, creating uniform superposition
2. **Measurement**: Collapses quantum state to obtain binary string
3. **Decoding**: Maps binary result to lottery number combinations

### Resource Requirements

For generating 4 games (6 numbers from 1-45):
- Possible single game combinations: 8,145,060
- Bits per game: 23
- Total qubits required: 92
- Superposition space: 2^92 states

## Installation

```bash
# Clone repository
git clone https://github.com/ryandau/qlottery.git
cd qlottery

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Create an IBM Quantum account at [quantum.cloud.ibm.com](https://quantum.cloud.ibm.com)
2. Obtain your API token from account settings
3. Run the generator and provide your token when prompted (saved for future use)

## Usage

### Command Line

```bash
python quantum_lottery_generator.py
```

### Python API

```python
from quantum_lottery_generator import QuantumLotteryGenerator

# Initialize generator
generator = QuantumLotteryGenerator(
    numbers_per_game=6,
    number_range=45,
    num_games=4
)

# Generate lottery games
result = generator.generate(token="your_ibm_quantum_token")

# Access results
for i, game in enumerate(result['games'], 1):
    print(f"Game {i}: {game}")

print(f"Backend used: {result['backend']}")
print(f"Quantum state: {result['quantum_state']}")
```

## Output Example

```
Quantum Multi-Game Lottery Generator
==================================================

RESULTS
==================================================
Game 1: [5, 12, 23, 31, 38, 44]
Game 2: [2, 15, 19, 27, 33, 42]
Game 3: [8, 14, 21, 29, 36, 41]
Game 4: [3, 11, 18, 26, 34, 45]

Quantum Details:
  Backend: ibm_brisbane
  Measurement: 101101...010
  Superposition size: 4,951,760,157,141,521,099,596,496,896 states
  Job ID: ch8x9y2z3a4b5c6d7e8f9g0h
```

## Architecture

```
QuantumLotteryGenerator
├── initialize_quantum_service()    # IBM Quantum connection
├── _calculate_quantum_requirements() # Circuit sizing
├── _create_quantum_circuit()       # Superposition creation
├── _decode_measurement()           # Result interpretation
└── generate()                      # Main execution pipeline
```

## Scientific Background

This implementation demonstrates:
- **Quantum Parallelism**: Simultaneous evaluation of all possible states
- **True Randomness**: Non-deterministic quantum measurement
- **State Collapse**: Observable quantum-to-classical transition
- **Superposition**: Coherent quantum state manipulation

## License

MIT License - see LICENSE file for details

## Disclaimer

This project is for educational and experimental purposes. The quantum number generation provides true randomness but does not influence lottery outcomes. Lottery games involve independent random draws.

## Acknowledgments

- IBM Quantum for providing quantum computing access
- Qiskit development team for the quantum computing framework

## Contact

For questions or suggestions, please open an issue on GitHub.
