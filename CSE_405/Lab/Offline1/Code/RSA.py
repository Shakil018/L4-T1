# from operator import inv
# from pwd import getpwuid
# from typing_extensions import IntVar
# from xml.dom.minidom import getDOMImplementation
# from typing_extensions import IntVar
# from typing_extensions import IntVar
from BitVector import *
# from numpy import _IntValue


def GenPrimePair(key_len):

    each_key_len = int(int(key_len)/2)
    while True:
        p1 = BitVector(intVal = 0)
        p1 = p1.gen_random_bits(each_key_len)
        probability = p1.test_for_primality()

        if probability > 0.0:
            break;
    
    while True:
        p2 = BitVector(intVal = 0)
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
        totient_bv = BitVector(intVal = totient)
        i_bv = BitVector(intVal = i)

        gcd_bv = totient_bv.gcd(i_bv)

        gcd_val = gcd_bv.intValue()
        
        if gcd_val == 1:
            public_key = i
            break

    return public_key



def GenPrivateKey(totient, public_key):

    private_key = -1

    modulus_bv = BitVector(intVal = totient)
    public_key_bv = BitVector(intVal = public_key) 
    private_key_bv = public_key_bv.multiplicative_inverse( modulus_bv )
    
    if private_key_bv is not None:
        print(str(int(private_key_bv))) 
        private_key = int(private_key_bv)
    else: 
        print("No multiplicative inverse in this case")


    return private_key



def GenCipherText(message, public_key, N, key_len):

    cipher_text = []
    
    for ch in message:
        ch_bv = BitVector(intVal = ord(ch))
        N_bv = BitVector(intVal = N)

        product_bv = BitVector(intVal = ord(ch))

        # print("{} char ascii value: {}".format(ch, product_bv.intValue()))
        # print("Before the power for loop")

        print("before loop")
        for _ in range(int(public_key)-1):
            product_bv = product_bv.gf_multiply_modular(ch_bv, N_bv, key_len)
        print("after the power for loop")

        ciphered_ch = product_bv.intValue()
        
        # print("cipher text: ", ciphered_ch)

        cipher_text.append(ciphered_ch)

    return cipher_text




def RSA_Encryption(message, key_len):
    prime1, prime2 = GenPrimePair(key_len=key_len)

    # prime1, prime2 = 45097, 2123962321
    # N = 2571216841

    N = prime1 * prime2

    # print("N : ", N)

    totient = (prime1 - 1) * (prime2 - 1)
    
    public_key = GenPublicKey(totient, key_len)

    private_key = GenPrivateKey(totient=totient, public_key=public_key)

    print("public key: {}, private key: {}".format(public_key, private_key))

    # public_key, private_key = 45097, 2123962321

    print("before cipher text")
    cipher_text = GenCipherText(message, public_key, N, key_len)
    print("after cipher text")

    return cipher_text, public_key, private_key, N






def RSA_Decryption(cipher_text, private_key, N, key_len):

    text = ''
    for cipher in cipher_text:
        ch_bv = BitVector(intVal = cipher)
        N_bv = BitVector(intVal = N)

        product_bv = BitVector(intVal = cipher)

        # print("{} char ascii value: {}".format(ch, product_bv.intValue()))
        # print("Before the power for loop")
        for _ in range(private_key-1):
            product_bv = ch_bv.gf_multiply_modular(product_bv, N_bv, key_len)
        # print("after the power for loop")

        text_ch = chr(product_bv.intValue())

        text += text_ch

    return text



# =====================================================================================
# =================================== Input ===========================================
# =====================================================================================
# key_len = 16, 32, 64, 128

key_len = input("Enter key length: ")
message = input("Enter your message: ")

cipher_text, public_key, private_key, N = RSA_Encryption(message, key_len)



print("Cipher text: ")
print(cipher_text)

decrypted_text = RSA_Decryption(cipher_text, private_key, N = N, key_len = key_len)

print("Decrypted Message: ", decrypted_text)

# print(ord(key_len))






# print("using mulplicative inverse: ")
# bv_modulus = BitVector(intVal = 140001)
# bv = BitVector(intVal = 941) 
# bv_result = bv.multiplicative_inverse( bv_modulus )
# if bv_result is not None:
#     print(str(int(bv_result)))           # 17
# else: 
#     print("No multiplicative inverse in this case")


# print("using gf_mi method: ")
# # modulus = BitVector(bitstring = '100011011')
# modulus = BitVector(hexstring="222E1")

# n = 40
# # a = BitVector(bitstring = '00110011')
# a = BitVector(hexstring = "3AD")
# multi_inverse = a.gf_MI(modulus, n)
# print(multi_inverse)                       # 01101100
    




# bv = BitVector(intVal = 0)
# bv = bv.gen_random_bits(16)  
# print(bv)
# print("hex value: ", bv.get_bitvector_in_hex())
# print("ascii value, ", bv.get_bitvector_in_ascii())
# check = bv.test_for_primality()
# print("if prime: ", check)  

# num = BitVector(intVal = 31, size = 8)
# print("{} is prime: {}".format(num, num.test_for_primality()))