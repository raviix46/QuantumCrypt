# 🛡️ QuantumCrypt

Welcome to the **QuantumCrypt** — a modern Gradio-based application that leverages principles of **quantum key distribution**, **post-quantum encryption**, and **visual quantum tools** to simulate a secure communication pipeline. This project integrates quantum concepts like the **BB84 protocol**, **Fernet key encryption**, and **intrusion detection using quantum circuits**, making it a perfect demonstrator for cybersecurity in the quantum era.

---

## 🚀 Project Overview

This project serves as an educational yet practical toolkit to understand how quantum principles can be harnessed for encryption and secure communication. It includes:

- **QKD Key Generation** using the BB84 protocol logic.
- **Secure Encryption and Decryption** using Fernet keys derived from QKD.
- **Quantum Intrusion Detection** using quantum circuit classifiers.
- **Randomness Visualization** for generated keys.
- **Simulated Eavesdropper Noise** to visualize attack scenarios.
- **Quantum Random Number Generation (QRNG)** using Hadamard gates.

---

## 🎯 Objectives

- Demonstrate the practicality of **quantum key distribution (QKD)** in generating secure cryptographic keys.
- Enable **secure message encryption and decryption** using Fernet keys derived from QKD-generated binary.
- Visualize **bit randomness** to assess entropy of generated keys.
- Simulate an **eavesdropper attack** and show visual impact on key integrity.
- Use **quantum circuits** to perform **intrusion detection** on external data streams.
- Offer a **user-friendly interface** built in Gradio with real-time QR code generation.

---

## 🧠 Methodology

The project is structured into modular components:

1. **QKD Key Generation**:
   - Implements the core BB84 principle: only when Alice’s and Bob’s bases match, the bit is accepted.
   - Output is a shared binary string acting as a secure key.

2. **Fernet Key Conversion**:
   - A 256-bit substring of the QKD key is encoded into a 32-byte Fernet key using Base64 encoding.

3. **Quantum Encryption**:
   - Message is encrypted using the Fernet key.
   - Generates a **QR Code** for the encrypted key to mimic secure transfer.

4. **Quantum Decryption**:
   - Message is decrypted using the corresponding Fernet key.

5. **Quantum Intrusion Detection**:
   - A small quantum classifier using parameterized RY rotations and a CNOT gate analyzes stream data.
   - Detects abnormal data patterns based on expectation values.

6. **Bit Randomness Visualizer**:
   - Plots bit values of a binary QKD key to assess how randomly they are distributed.

7. **Eavesdropper Noise Simulation**:
   - Simulates attack by flipping a percentage of bits in the QKD key.
   - Plots original vs. noisy key for comparison.

8. **Quantum Random Number Generator**:
   - Uses Qiskit's Hadamard gate to simulate quantum coin-flips.

---

## 🧩 Project Modules

| Module                        | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| `generate_qkd_key()`         | Generates QKD key based on basis match logic.                               |
| `bb84_to_fernet_key()`       | Converts binary string to a 32-byte Fernet-compatible Base64 key.           |
| `quantum_encrypt()`          | Encrypts text using QKD-derived Fernet key.                                |
| `quantum_decrypt()`          | Decrypts message using Fernet key.                                          |
| `generate_qr_image()`        | Generates QR code from the encryption key.                                  |
| `quantum_intrusion_detection()` | Uses quantum classifier to flag abnormal inputs.                        |
| `plot_key_bits()`            | Visualizes randomness of key bits.                                          |
| `compare_original_vs_noisy()`| Compares clean and noisy keys to simulate attacks.                         |
| `quantum_random_number()`    | Returns single random bit using Qiskit’s simulator.                         |


---

## 🔧 Tech Stack

- **Python 3.10+**
- **Gradio** (for interactive GUI)
- **Qiskit** (for quantum circuit simulations)
- **PennyLane** (for hybrid quantum-classical circuits)
- **Cryptography** (for Fernet symmetric encryption)
- **Matplotlib** (for key visualization)
- **qrcode / Pillow** (for QR Code generation)

---

## 📈 Future Work

- Add **download buttons** for encrypted messages and keys.
- Enable **file encryption** in addition to text messages.
- Allow **custom QKD keys** to be uploaded by the user.
- Extend intrusion detection with **more qubits and datasets**.
- Add **copy-to-clipboard** features on all output boxes.
- Deploy full version on **Hugging Face Spaces**.

---

## 📑 References

1. Bennett, C. H., & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing." *Proceedings of IEEE International Conference on Computers, Systems and Signal Processing*, Bangalore, India.
2. Fernet symmetric encryption: https://cryptography.io/en/latest/fernet/
3. Qiskit Documentation: https://qiskit.org/documentation/
4. PennyLane Documentation: https://docs.pennylane.ai/
5. Gradio: https://www.gradio.app/
6. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
