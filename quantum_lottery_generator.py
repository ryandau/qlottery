"""
Quantum Multi-Game Lottery Generator

Generates multiple lottery game combinations using quantum superposition and measurement
on IBM Quantum hardware. Demonstrates practical application of quantum computing for
generating truly random number combinations through quantum state collapse.

Author: Ryan Donohue
License: MIT
"""

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import itertools
from math import log2, ceil
from typing import List, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # Simplified format without timestamps
)
logger = logging.getLogger(__name__)

# Suppress verbose logs from Qiskit and IBM libraries
logging.getLogger('qiskit').setLevel(logging.ERROR)
logging.getLogger('qiskit_ibm_runtime').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('websocket').setLevel(logging.WARNING)


class QuantumLotteryGenerator:
    """
    Generates lottery number combinations using quantum superposition.
    
    This implementation uses IBM Quantum hardware to generate multiple lottery
    games simultaneously through a single quantum measurement, leveraging quantum
    superposition and state collapse for true randomness.
    """
    
    def __init__(self, numbers_per_game: int = 6, number_range: int = 45, num_games: int = 4):
        """
        Initialise the quantum lottery generator.
        
        Args:
            numbers_per_game: Number of selections per game
            number_range: Maximum number in lottery range (1 to number_range)
            num_games: Number of games to generate simultaneously
        """
        self.numbers_per_game = numbers_per_game
        self.number_range = number_range
        self.num_games = num_games
        self.service = None
        
    def initialize_quantum_service(self, token: str = None, instance: str = None) -> QiskitRuntimeService:
        """
        Initialize connection to IBM Quantum service.
        
        Args:
            token: IBM Quantum API token (optional if already saved)
            instance: IBM Quantum instance (CRN) - optional
            
        Returns:
            QiskitRuntimeService instance
            
        Raises:
            Exception: If connection fails
        """
        try:
            # Try connecting with existing credentials
            if instance:
                self.service = QiskitRuntimeService(instance=instance)
            else:
                self.service = QiskitRuntimeService()
            logger.info("Successfully connected to IBM Quantum service")
            return self.service
        except Exception as e:
            if token:
                try:
                    # Save new credentials
                    QiskitRuntimeService.save_account(
                        channel="ibm_quantum_platform", 
                        token=token,
                        overwrite=True,
                        instance=instance
                    )
                    # Try connecting again
                    if instance:
                        self.service = QiskitRuntimeService(instance=instance)
                    else:
                        self.service = QiskitRuntimeService()
                    logger.info("Credentials saved and connected to IBM Quantum service")
                    return self.service
                except Exception as save_error:
                    logger.error(f"Failed to save credentials: {save_error}")
                    logger.info("Hint: You may need to provide your instance CRN. Find it at: https://quantum.cloud.ibm.com")
                    raise
            else:
                logger.error("IBM Quantum credentials not found. Please provide API token.")
                logger.info("Get your token at: https://quantum.cloud.ibm.com")
                raise
    
    def _calculate_quantum_requirements(self) -> Tuple[List[Tuple], int, int]:
        """
        Calculate quantum circuit requirements for generating multiple games.
        
        Returns:
            Tuple containing:
                - List of all possible single game combinations
                - Bits required per game
                - Total qubits needed
        """
        single_games = list(itertools.combinations(
            range(1, self.number_range + 1), 
            self.numbers_per_game
        ))
        
        bits_per_game = ceil(log2(len(single_games)))
        total_bits = bits_per_game * self.num_games
        
        logger.info(f"Quantum requirements: {total_bits} qubits "
                   f"({bits_per_game} bits per game, {len(single_games)} possible combinations)")
        
        return single_games, bits_per_game, total_bits
    
    def _create_quantum_circuit(self, num_qubits: int) -> QuantumCircuit:
        """
        Create quantum circuit with full superposition.
        
        Args:
            num_qubits: Number of qubits to use
            
        Returns:
            Configured QuantumCircuit
        """
        qc = QuantumCircuit(num_qubits)
        
        # Apply Hadamard gates to create superposition across all qubits
        for i in range(num_qubits):
            qc.h(i)
        
        qc.measure_all()
        
        logger.info(f"Created quantum circuit with {num_qubits}-dimensional superposition "
                   f"({2**num_qubits:,} possible states)")
        
        return qc
    
    def _decode_measurement(self, binary_result: str, single_games: List[Tuple], 
                           bits_per_game: int) -> List[List[int]]:
        """
        Decode quantum measurement result into lottery games.
        
        Args:
            binary_result: Binary string from quantum measurement
            single_games: List of all possible single game combinations
            bits_per_game: Number of bits encoding each game
            
        Returns:
            List of lottery number combinations
        """
        games = []
        
        for game_num in range(self.num_games):
            start_bit = game_num * bits_per_game
            end_bit = start_bit + bits_per_game
            game_bits = binary_result[start_bit:end_bit]
            
            game_index = int(game_bits, 2) % len(single_games)
            lottery_numbers = sorted(list(single_games[game_index]))
            games.append(lottery_numbers)
            
            logger.debug(f"Game {game_num + 1}: bits={game_bits}, "
                        f"index={game_index}, numbers={lottery_numbers}")
        
        return games
    
    def generate(self, token: str = None, backend_name: str = None, instance: str = None) -> dict:
        """
        Generate lottery games using quantum measurement.
        
        Args:
            token: IBM Quantum API token (optional)
            backend_name: Specific backend to use (optional, defaults to least busy)
            instance: IBM Quantum instance CRN (optional)
            
        Returns:
            Dictionary containing:
                - games: List of generated lottery number combinations
                - quantum_state: Binary measurement result
                - backend: Name of quantum computer used
                - metadata: Additional quantum execution details
        """
        # Initialize service
        if not self.service:
            self.initialize_quantum_service(token, instance)
        
        # Calculate requirements
        single_games, bits_per_game, total_bits = self._calculate_quantum_requirements()
        
        # Select backend
        if backend_name:
            backend = self.service.backend(backend_name)
        else:
            backend = self.service.least_busy(
                operational=True, 
                min_num_qubits=total_bits
            )
        
        logger.info(f"Selected quantum backend: {backend.name}")
        
        # Create and compile circuit
        qc = self._create_quantum_circuit(total_bits)
        compiled_qc = transpile(qc, backend, optimization_level=3)
        
        # Execute on quantum hardware
        logger.info(f"Executing quantum circuit on {backend.name}")
        sampler = Sampler(backend)
        job = sampler.run([compiled_qc], shots=1)
        
        logger.info(f"Job submitted: {job.job_id()}")
        
        # Retrieve results
        result = job.result()
        counts = result[0].data.meas.get_counts()
        binary_result = list(counts.keys())[0]
        
        logger.info(f"Quantum measurement complete: {binary_result}")
        
        # Decode into games
        games = self._decode_measurement(binary_result, single_games, bits_per_game)
        
        return {
            'games': games,
            'quantum_state': binary_result,
            'backend': backend.name,
            'metadata': {
                'num_qubits': total_bits,
                'bits_per_game': bits_per_game,
                'superposition_size': 2**total_bits,
                'job_id': job.job_id()
            }
        }


def main():
    """Command-line interface for quantum lottery generator."""
    print("Quantum Multi-Game Lottery Generator")
    print("=" * 50)
    print("\nConfiguration:")
    print("  - Numbers per game: 6")
    print("  - Number range: 1-45")
    print("  - Games per ticket: 4")
    print("\nRequirements:")
    print("  - IBM Quantum account (https://quantum.cloud.ibm.com)")
    print("  - API token from account settings")
    print("  - Package: qiskit-ibm-runtime")
    print()
    
    try:
        token = input("Enter IBM Quantum API token (or press Enter if already configured): ").strip()
        token = token if token else None
        
        generator = QuantumLotteryGenerator(
            numbers_per_game=6,
            number_range=45,
            num_games=4
        )
        
        # Try to generate with just the token first
        try:
            result = generator.generate(token=token)
        except Exception as e:
            # If it fails and mentions instance, ask for it
            if "instance" in str(e).lower() or "No matching instances" in str(e):
                print("\nYour account may require an instance CRN.")
                print("Find it at: https://quantum.cloud.ibm.com (under Account settings)")
                instance = input("Enter instance CRN (or press Enter to skip): ").strip()
                instance = instance if instance else None
                result = generator.generate(token=token, instance=instance)
            else:
                raise
        
        print("\n" + "=" * 50)
        print("RESULTS")
        print("=" * 50)
        
        for i, game in enumerate(result['games'], 1):
            print(f"Game {i}: {game}")
        
        print(f"\nQuantum Details:")
        print(f"  Backend: {result['backend']}")
        print(f"  Measurement: {result['quantum_state']}")
        print(f"  Superposition size: {result['metadata']['superposition_size']:,} states")
        print(f"  Job ID: {result['metadata']['job_id']}")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        raise


if __name__ == "__main__":
    main()
