from block_function import state_builder, block_function, serialize, next_state


def chacha20_encrypt(key: int, counter: int, nonce: int, plaintext: bytes) -> bytes:
    """
    Chiffre un message avec l’algorithme ChaCha20.

    ChaCha20 génère un flot de clés de 64 octets (512 bits) par appel à la fonction de bloc,
    puis applique un XOR entre ce flot et le texte clair.

    :param key: la clé (256 bits).
    :param counter: le compteur de blocs initial (32 bits).
        Note : Cette valeur peut être définie comme étant n'importe quel nombre, mais sera généralement zéro ou un.
               Il est logique d'utiliser un si le bloc zéro est utilisé pour autre chose, comme générer une clé
               d'authentification à usage unique (dans le cadre d'un )algorithme AEAD).
    :param nonce: le nonce (96 bits).
    :param plaintext: le texte clair à chiffrer.
    :return: le texte chiffré (même longueur que `plaintext`).
    """
    plaintext_int = int.from_bytes(plaintext, byteorder='big')
    plaintext_len = len(plaintext)
    
    state = state_builder(key, counter, nonce)
    
    keystream = 0
    num_blocks = (plaintext_len + 63) // 64
    
    current_state = state
    for i in range(num_blocks):
        block = block_function(current_state)
        serialized_block = serialize(block)
        
        keystream = (keystream << 512) | serialized_block
        
        current_state = next_state(current_state)
    
    total_keystream_bits = num_blocks * 512
    plaintext_bits = plaintext_len * 8
    
    if total_keystream_bits > plaintext_bits:
        keystream = keystream >> (total_keystream_bits - plaintext_bits)
    
    ciphertext_int = plaintext_int ^ keystream
    
    ciphertext = ciphertext_int.to_bytes(plaintext_len, byteorder='big')
    
    return ciphertext
