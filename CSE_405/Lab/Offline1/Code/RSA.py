from BitVector import *
import time

time_start = 0;
key_generation_time = 0
encryption_time = 0
decryption_time = 0



def GenPrimePair(key_len):
    each_key_len = int(int(key_len) / 2)
    while True:
        p1 = BitVector(intVal=0)
        p1 = p1.gen_random_bits(each_key_len)
        probability = p1.test_for_primality()

        if probability > 0.0:
            break;

    while True:
        p2 = BitVector(intVal=0)
        p2 = p2.gen_random_bits(each_key_len)
        if p2 == p1:
            continue
        probability = p2.test_for_primality()

        if probability > 0.0:
            break;

    print("prime 1: ", p1.get_bitvector_in_hex())
    print("prime 2: ", p2.get_bitvector_in_hex())

    return p1.intValue(), p2.intValue()


def GenPublicKey(totient, key_len):
    public_key = -1

    for i in range(2, totient):
        totient_bv = BitVector(intVal=totient)
        i_bv = BitVector(intVal=i)

        gcd_bv = totient_bv.gcd(i_bv)

        gcd_val = gcd_bv.intValue()

        if gcd_val == 1:
            public_key = i
            break

    return public_key


def GenPrivateKey(totient, public_key):
    private_key = -1

    modulus_bv = BitVector(intVal=totient)
    public_key_bv = BitVector(intVal=public_key)
    private_key_bv = public_key_bv.multiplicative_inverse(modulus_bv)

    if private_key_bv is not None:
        print(str(int(private_key_bv)))
        private_key = int(private_key_bv)
    else:
        print("No multiplicative inverse in this case")

    return private_key


def GenCipherText(message, public_key, N, key_len):
    cipher_text = []

    for ch in message:
        ciphered_ch = int(pow(ord(ch), public_key, N))
        cipher_text.append(ciphered_ch)

    return cipher_text


def RSA_Encryption(message, key_len):

    global key_generation_time, encryption_time

    time_start = time.time()

    prime1, prime2 = GenPrimePair(key_len=key_len)

    N = prime1 * prime2

    totient = (prime1 - 1) * (prime2 - 1)
    public_key = GenPublicKey(totient, key_len)
    private_key = GenPrivateKey(totient=totient, public_key=public_key)

    key_generation_time = time.time() - time_start

    time_start = time.time()
    cipher_text = GenCipherText(message, public_key, N, key_len)
    encryption_time = time.time() - time_start

    return cipher_text, public_key, private_key, N


def RSA_Decryption(cipher_text, private_key, N):
    global decryption_time

    time_start = time.time()
    text = ''
    for cipher in cipher_text:
        deciphered_ch = chr(int(pow(int(cipher), int(private_key), int(N) )))
        text += deciphered_ch

    decryption_time = time.time() - time_start

    return text



def print_hex(message):
    msg = ''

    for ch in message:
        bv = BitVector(intVal = ord(ch), size = 8)
        ch2 = bv.get_bitvector_in_hex()
        msg += ch2

    print(msg)



# =====================================================================================
# =================================== Input ===========================================
# =====================================================================================
# key_len = 16, 32, 64, 128


def main():
    global key_generation_time, encryption_time, decryption_time

    print("1. Input Plain Text: ")
    print("2. Input File")

    option = input("Enter choice: ")

    key_list = [16, 32, 64, 128]
    time_list = []

    if int(option) == 1:
        message = input("Enter Plain Text:  ")


        for key_len in key_list:

            print("\n Key Length: {}".format(key_len))
            cipher_text, public_key, private_key, N = RSA_Encryption(message, key_len)


            print("Plain text:")
            print(message)
            print_hex(message)

            print("\nKey: ")
            print("public key:[ {}, {} ], private key: [{}, {}]".format(public_key, N, private_key, N))

            print("Cipher text: ")
            print(cipher_text)

            decrypted_text = RSA_Decryption(cipher_text, private_key, N=N)
            print("Deciphered Text: ")
            print_hex(decrypted_text)
            print(decrypted_text)

            time_list.append([key_generation_time, encryption_time, decryption_time])


        print("K    key-gen-time    enc-time    dec-time")
        for i in range(4):
            print("{}       {}     {}     {}".format(key_list[i], time_list[i][0], time_list[i][1], time_list[i][2]))



    elif int(option) == 2:
        fileDir = input("Enter filename: ")
        #
        # time_start = time.time()
        # encrypted_file = EncryptFile(fileDir)
        # encryption_time = time.time() - time_start
        #
        # time_start = time.time()
        # DecryptFile(encrypted_file, fileDir)
        # decryption_time = time.time() - time_start

    else:
        print("Unknown Command")

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()

