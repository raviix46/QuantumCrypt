import numpy as np
import gradio as gr
import pennylane as qml
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from cryptography.fernet import Fernet
import random
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import qrcode

# 1. Generate QKD Key (BB84 protocol with matching basis logic)
def generate_qkd_key(length=128):
    shared_key = ""
    while len(shared_key) < length:
        alice_bit = random.randint(0, 1)
        alice_basis = random.randint(0, 1)
        bob_basis = random.randint(0, 1)
        if alice_basis == bob_basis:
            shared_key += str(alice_bit)
    return shared_key

# 2. Convert to Fernet Key
def bb84_to_fernet_key(qkey_binary_str):
    if len(qkey_binary_str) < 256:
        raise ValueError("QKD key must be at least 256 bits for Fernet encryption.")
    binary_256 = qkey_binary_str[:256]
    int_val = int(binary_256, 2)
    byte_val = int_val.to_bytes(32, 'big')
    fernet_key = base64.urlsafe_b64encode(byte_val)
    if len(fernet_key) != 44:
        raise ValueError("Invalid Fernet key length.")
    return fernet_key

# 3. Encrypt
def quantum_encrypt(message, qkd_key):
    if not qkd_key or len(qkd_key) < 72:
        return "❌ QKD key too short. Minimum 72 bits required.", "", None
    try:
        fernet_key = bb84_to_fernet_key(qkd_key)
        f = Fernet(fernet_key)
        encrypted_message = f.encrypt(message.encode())
        qr_img = generate_qr_image(fernet_key.decode())
        return encrypted_message.decode(), fernet_key.decode(), qr_img
    except Exception as e:
        return f"Encryption error: {str(e)}", "", None

# 4. Decrypt
def quantum_decrypt(encrypted_message, key):
    try:
        f = Fernet(key.encode())
        return f.decrypt(encrypted_message.encode()).decode()
    except Exception as e:
        return f"Decryption error: {str(e)}"

# 5. QR Code Generator
def generate_qr_image(data):
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Image.open(buf)

# 6. Quantum Intrusion Detection
def quantum_intrusion_detection(data_stream):
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def classifier(x):
        qml.RY(x[0], wires=0)
        qml.RY(x[1], wires=1)
        qml.CNOT(wires=[0, 1])
        return qml.expval(qml.PauliZ(0))

    try:
        x = [float(i) for i in data_stream.split(',')]
        score = abs(classifier(x))
        return "🚨 Intrusion Detected" if score > 0.7 else "✅ Normal Activity"
    except:
        return "❌ Invalid input. Format: 0.3,0.7"

# 7. Randomness Visualizer
def plot_key_bits(key_str):
    bits = [int(b) for b in key_str.strip() if b in '01']
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.bar(range(len(bits)), bits, color='skyblue')
    ax.set_title("Bit Distribution of QKD Key")
    ax.set_xlabel("Bit Index")
    ax.set_ylabel("Bit Value")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return Image.open(buf)

# 8. Eavesdropper Noise Simulation
def add_noise_to_key(key_str, flip_percent=0.05):
    bits = list(key_str.strip())
    total_bits = len(bits)
    num_flips = int(total_bits * flip_percent)
    flip_indices = random.sample(range(total_bits), num_flips)
    for i in flip_indices:
        bits[i] = '1' if bits[i] == '0' else '0'
    return ''.join(bits)

def compare_original_vs_noisy(key_str):
    noisy_key = add_noise_to_key(key_str)
    fig, axs = plt.subplots(2, 1, figsize=(10, 4), sharex=True)
    axs[0].bar(range(len(key_str)), [int(b) for b in key_str], color='green')
    axs[0].set_title("Original QKD Key")
    axs[1].bar(range(len(noisy_key)), [int(b) for b in noisy_key], color='red')
    axs[1].set_title("QKD Key After Eavesdropper Noise")
    axs[1].set_xlabel("Bit Index")
    axs[0].set_ylabel("Bit Value")
    axs[1].set_ylabel("Bit Value")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return Image.open(buf)

# 9. Quantum Random Number Generator
def quantum_random_number():
    backend = Aer.get_backend('aer_simulator')
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    job = backend.run(circuit, shots=1)
    result = job.result()
    counts = result.get_counts()
    return list(counts.keys())[0]

# 10. Gradio Interface
def create_interface():
    with gr.Blocks(title="QuantumCrypt") as demo:
        gr.Markdown("# 🛡️ QuantumCrypt")

        qkd_key_state = gr.State("")

        # Tab 1: QKD Key Generation
        with gr.Tab("1️⃣ Quantum Key Distribution"):
            key_length = gr.Slider(72, 512, step=8, value=128, label="Select QKD Key Length (≥ 72 bits)")
            qkd_btn = gr.Button("Generate Quantum Key")
            qkd_output = gr.Textbox(label="Generated QKD Key")

            def generate_and_store_key(length):
                key = generate_qkd_key(length)
                return key, key

            qkd_btn.click(generate_and_store_key,
                          inputs=[key_length],
                          outputs=[qkd_output, qkd_key_state])

        # Tab 2: Encryption
        with gr.Tab("2️⃣ Quantum Encryption"):
            msg_input = gr.Textbox(label="Message to Encrypt")
            encrypt_btn = gr.Button("Encrypt with QKD Key")
            encrypted_output = gr.Textbox(label="Encrypted Message")
            key_used_output = gr.Textbox(label="Fernet Key Used")
            qr_code_output = gr.Image(label="QR Code of Key")

            encrypt_btn.click(quantum_encrypt,
                              inputs=[msg_input, qkd_key_state],
                              outputs=[encrypted_output, key_used_output, qr_code_output])

        # Tab 3: Decryption
        with gr.Tab("3️⃣ Quantum Decryption"):
            encrypted_input = gr.Textbox(label="Encrypted Message")
            key_input = gr.Textbox(label="Fernet Key")
            decrypt_btn = gr.Button("Decrypt")
            decrypted_output = gr.Textbox(label="Decrypted Message")

            decrypt_btn.click(quantum_decrypt,
                              inputs=[encrypted_input, key_input],
                              outputs=[decrypted_output])

        # Tab 4: Intrusion Detection
        with gr.Tab("4️⃣ Quantum Intrusion Detection"):
            data_input = gr.Textbox(label="Data Stream (e.g. 0.3,0.7)")
            detect_btn = gr.Button("Analyze")
            detection_output = gr.Textbox(label="Detection Result")
            detect_btn.click(quantum_intrusion_detection,
                             inputs=[data_input],
                             outputs=[detection_output])

        # Tab 5: Quantum Randomness Visualizer
        with gr.Tab("📊 QKD Key Randomness Visualizer"):
            binary_input = gr.Textbox(label="Enter QKD Key (binary)", lines=3)
            visualize_btn = gr.Button("Plot Bit Distribution")
            graph_output = gr.Image(label="Randomness Graph")
            visualize_btn.click(plot_key_bits, inputs=[binary_input], outputs=[graph_output])

        # Tab 6: Eavesdropper Noise Simulation
        with gr.Tab("📉 Eavesdropper Noise Simulation"):
            original_input = gr.Textbox(label="Enter QKD Key (binary)", lines=3)
            noise_btn = gr.Button("Simulate Eavesdropper")
            noise_graph = gr.Image(label="Original vs Noisy")
            noise_btn.click(compare_original_vs_noisy, inputs=[original_input], outputs=[noise_graph])

    return demo

# 11. Launch App
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=True)
