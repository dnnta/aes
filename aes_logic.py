from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

class Step:
    def __init__(self, round, detail):
        self.round = round
        self.detail = detail

def validate_key(key_str):
    key_bytes = key_str.encode('utf-8')
    if len(key_bytes) not in [16, 24, 32]:
        raise ValueError("Key must be 16 (AES-128), 24 (AES-192), or 32 (AES-256) bytes long.")
    return key_bytes

def get_aes_round_steps(key_len_bits):
    rounds = 10 if key_len_bits == 128 else 12 if key_len_bits == 192 else 14
    step_list = []

    step_list.append(Step("Round 0", "AddRoundKey"))

    for r in range(1, rounds):
        step_list.append(Step(f"Round {r}", "SubBytes → ShiftRows → MixColumns → AddRoundKey"))

    step_list.append(Step(f"Final Round", "SubBytes → ShiftRows → AddRoundKey"))

    return step_list

def encrypt_aes(plaintext, key_str, mode):
    key = validate_key(key_str)
    plaintext_bytes = plaintext.encode('utf-8')
    padded_data = pad(plaintext_bytes, AES.block_size)

    steps = []

    if mode == 'ECB':
        cipher = AES.new(key, AES.MODE_ECB)
        steps.append(Step("Input", f"Plaintext: {plaintext}"))
        steps.append(Step("Mode", "ECB"))
        steps.append(Step("Key", key.hex()))
        ciphertext = cipher.encrypt(padded_data)

    elif mode == 'CBC':
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        steps.append(Step("Input", f"Plaintext: {plaintext}"))
        steps.append(Step("Mode", "CBC"))
        steps.append(Step("IV", iv.hex()))
        steps.append(Step("Key", key.hex()))
        ciphertext = iv + cipher.encrypt(padded_data)
    else:
        raise ValueError("Unsupported mode. Choose ECB or CBC.")

    # AES structure for teaching
    key_len_bits = len(key) * 8
    steps.extend(get_aes_round_steps(key_len_bits))

    # Final output
    steps.append(Step("Ciphertext (Base64)", base64.b64encode(ciphertext).decode()))
    return base64.b64encode(ciphertext).decode(), steps

def decrypt_aes(ciphertext_b64, key_str, mode):
    key = validate_key(key_str)
    ciphertext = base64.b64decode(ciphertext_b64)
    steps = []

    if mode == 'ECB':
        cipher = AES.new(key, AES.MODE_ECB)
        steps.append(Step("Mode", "ECB"))
        steps.append(Step("Key", key.hex()))
        plaintext_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
    elif mode == 'CBC':
        iv = ciphertext[:16]
        real_ciphertext = ciphertext[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        steps.append(Step("Mode", "CBC"))
        steps.append(Step("IV", iv.hex()))
        steps.append(Step("Key", key.hex()))
        plaintext_bytes = unpad(cipher.decrypt(real_ciphertext), AES.block_size)
    else:
        raise ValueError("Unsupported mode. Choose ECB or CBC.")

    plaintext = plaintext_bytes.decode('utf-8')
    steps.append(Step("Decrypted Text", plaintext))

    return plaintext, steps
