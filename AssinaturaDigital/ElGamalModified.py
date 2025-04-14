import random
from sympy import isprime, mod_inverse
from math import prod

# Geração de número primo aleatório grande
def generate_large_prime(start=1000, end=5000):
    while True:
        p = random.randint(start, end)
        if isprime(p):
            return p

# Geração de chaves
def generate_keys():
    P = generate_large_prime()
    g = random.randint(2, P - 2)
    a = random.randint(2, P - 2)  # chave privada do destinatário
    b = pow(g, a, P)              # chave pública
    return {'P': P, 'g': g, 'a': a, 'b': b}

# Criptografia com múltiplos signatários
def encrypt_multi(P, g, b, m, R_list):
    c1_list = [pow(g, R, P) for R in R_list]

    b_expo_even = [pow(b, R_list[i], P) for i in range(len(R_list)) if i % 2 == 1]
    b_expo_odd = [pow(b, R_list[i], P) for i in range(len(R_list)) if i % 2 == 0]

    numerator = m * prod(b_expo_even) % P
    denominator = prod(b_expo_odd) % P
    c2 = numerator * mod_inverse(denominator, P) % P

    return c1_list, c2

# Descriptografia pelo destinatário
def decrypt_multi(P, a, c1_list, c2):
    c1_exp_odd = [pow(c1_list[i], a, P) for i in range(len(c1_list)) if i % 2 == 0]
    c1_exp_even = [pow(c1_list[i], a, P) for i in range(len(c1_list)) if i % 2 == 1]

    numerator = c2 * prod(c1_exp_odd) % P
    denominator = prod(c1_exp_even) % P
    m = numerator * mod_inverse(denominator, P) % P

    return m

# Simulação de teste
def simulate():
    print("🔐 Gerando chaves para o destinatário...")
    keys = generate_keys()
    P, g, a, b = keys['P'], keys['g'], keys['a'], keys['b']

    print(f"P = {P}, g = {g}, a = {a}, b = {b}")
    m = random.randint(1, P - 1)
    print(f"Mensagem original: {m}")

    num_signers = 5
    R_list = [random.randint(2, P - 2) for _ in range(num_signers)]

    print("\n🔏 Realizando criptografia...")
    c1_list, c2 = encrypt_multi(P, g, b, m, R_list)
    print(f"c1_list = {c1_list}")
    print(f"c2 = {c2}")

    print("\n🔓 Realizando descriptografia...")
    decrypted = decrypt_multi(P, a, c1_list, c2)
    print(f"Mensagem decriptada: {decrypted}")

    assert m == decrypted, "Erro: a mensagem decriptada não bate com a original"
    print("\n✅ Sucesso: Mensagem recuperada corretamente!")

# Rodar simulação
if __name__ == "__main__":
    simulate()
