# from string import hexdigits
from BitVector import *
import time

key_word_len = 4
num_rounds = 11
rcon_num = 10
rcon = []
key_matrix = []
padded_count = 0
cipher_padding = 0

time_start = 0;
key_scheduling_time = 0
encryption_time = 0
decryption_time = 0



Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"),
     BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"),
     BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"),
     BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"),
     BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"),
     BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"),
     BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"),
     BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"),
     BitVector(hexstring="09"), BitVector(hexstring="0E")]
]


def rcon_calc(size):
    rcon = []
    for i in range(1, size + 1):
        if i == 1:
            rcon.append(hex(1))
        elif int(rcon[i - 2], 16) < 80:
            temp = int(rcon[i - 2], 16) * 2
            rcon.append(hex(temp))
        elif int(rcon[i - 2], 16) > 80:
            temp = int(rcon[i - 2], 16) * 2
            temp = temp ^ int('0x11b', 16)
            rcon.append(hex(temp))

        # print(rcon[i-1])
        # print(int(rcon[i-1], 16))

    rcon_arr = []
    for i in range(1, size + 1):
        rcon_arr.append([rcon[i - 1], hex(00), hex(00), hex(00)])

    # print("final rcon, ", rcon_arr)

    return rcon_arr


def SubSboxVal(state_matrix, SMatrix):
    for j in range(4):
        for k in range(4):
            int_val = int(state_matrix[j][k], 16)
            s = SMatrix[int_val]
            state_matrix[j][k] = hex(s)

    # print("After sbox subs, ", state_matrix)

    return state_matrix


def CyclicRotation(state_matrix):
    # 2nd row
    state_matrix[1] = state_matrix[1][1:] + [state_matrix[1][0]]

    # 3rd row
    state_matrix[2] = state_matrix[2][2:] + state_matrix[2][:2]

    # 4th row:
    state_matrix[3] = [state_matrix[3][3]] + state_matrix[3][:3]

    # print("After cyclic rotation, ", state_matrix)

    return state_matrix


def InverseCyclic(state_matrix):
    # 2nd row:
    state_matrix[1] = [state_matrix[1][3]] + state_matrix[1][:3]

    # 3rd row:
    state_matrix[2] = state_matrix[2][2:] + state_matrix[2][:2]

    # 4th row:
    state_matrix[3] = state_matrix[3][1:] + [state_matrix[3][0]]

    return state_matrix


def Mixing(state_matrix, SMatrix):
    temp_matrix = []

    for j in range(4):
        temp2 = []
        for k in range(4):
            temp2.append(state_matrix[j][k])
        temp_matrix.append(temp2)

    # temp_matrix = [ state_matrix[j] for j in range(4)  ]

    # print("temp_matrix: ", temp_matrix)

    for j in range(4):
        for k in range(4):
            state_matrix[j][k] = BitVector(hexstring="00")
            for m in range(4):
                modulus = BitVector(bitstring='100011011')

                temp = BitVector(intVal=int(str(temp_matrix[m][k]), 16), size=8)
                state_matrix[j][k] ^= SMatrix[j][m].gf_multiply_modular(temp, modulus, 8)

                # state_matrix[j][k] = hex(state_matrix[j][k])
            state_matrix[j][k] = state_matrix[j][k].get_bitvector_in_hex()

    # print("after mixing state_matrix: ")
    # print(state_matrix)

    return state_matrix


def AddingRoundKey(state_matrix, index):
    global key_matrix

    # print("round key matrix: ")
    # print(key_matrix[index])
    # print("state matrix ", state_matrix)

    for j in range(4):
        for k in range(4):
            state_matrix[j][k] = hex(int(state_matrix[j][k], 16) ^ int(key_matrix[index][j][k], 16))

    # print("After adding round key: {}".format(index))
    # print(state_matrix)

    return state_matrix


def AES_encryption(state_matrix):
    global key_matrix, num_rounds

    # All round simulation:

    # Round 0:

    for i in range(4):
        for j in range(4):
            state_matrix[i][j] = hex(int(state_matrix[i][j], 16) ^ int(key_matrix[0][i][j], 16))

    # print("after round 0 ", state_matrix)

    for i in range(1, num_rounds):

        # Substituting sBox Value:
        state_matrix = SubSboxVal(state_matrix, Sbox)

        # cyclic rotation:
        state_matrix = CyclicRotation(state_matrix)

        # Mixing:
        if i != (num_rounds - 1):
            state_matrix = Mixing(state_matrix=state_matrix, SMatrix=Mixer)

        # Adding Round key:
        state_matrix = AddingRoundKey(state_matrix, i)

    return state_matrix


def AES_decryption(state_matrix):
    global key_matrix, num_rounds

    # All round simulation:

    # Round 0:

    for i in range(4):
        for j in range(4):
            state_matrix[i][j] = hex(int(state_matrix[i][j], 16) ^ int(key_matrix[num_rounds - 1][i][j], 16))

    for i in range(num_rounds - 2, -1, -1):

        # Inverse Shift Row:
        state_matrix = InverseCyclic(state_matrix=state_matrix)

        # Inverse Sub Bytes
        state_matrix = SubSboxVal(state_matrix=state_matrix, SMatrix=InvSbox)

        # Add round keys
        state_matrix = AddingRoundKey(state_matrix=state_matrix, index=i)

        # Inverse Mix cols:
        if i != 0:
            state_matrix = Mixing(state_matrix=state_matrix, SMatrix=InvMixer)

    return state_matrix


def print_message(message):
    msg = ''
    for i in range(len(message)):
        chunk = message[i]
        for j in range(4):
            for k in range(4):
                ch = chr(int(chunk[k][j], 16))
                msg += ch
    print(msg)

    return msg



def print_cipher_hex(message):
    global cipher_padding

    msg = ''
    cnt = 0
    limit = len(message)*16 - cipher_padding
    for i in range(len(message)):
        chunk = message[i]
        for j in range(4):
            for k in range(4):
                if cnt == limit:
                    break
                cnt += 1
                bv = BitVector(intVal=int(chunk[k][j], 16), size=8)
                ch2 = bv.get_bitvector_in_hex()
                msg += ch2
                # ch = chr(int(chunk[k][j], 16))
                # msg += ch
    print(msg)

    return msg


def print_hex(message):
    msg = ''

    for ch in message:
        bv = BitVector(intVal = ord(ch), size = 8)
        ch2 = bv.get_bitvector_in_hex()
        msg += ch2

    print(msg)



def StateMatrixGeneration(message_hex):
    state_matrix = []

    for i in range(0, 4):
        temp = [message_hex[j * 4 + i] for j in range(4)]
        state_matrix.append(temp)

    return state_matrix


def EncryptMessage(input_message):
    global key_matrix, num_rounds, cipher_padding

    message_hex = []
    for ch in input_message:
        message_hex.append(hex(ord(ch)))

    state_matrix = []

    if len(message_hex) <= 16:
        for _ in range(16 - len(message_hex)):
            message_hex.append(hex(ord(' ')))

            # print("message_hex: ")
            # print(message_hex)

        temp_matrix = StateMatrixGeneration(message_hex)

        state_matrix.append(AES_encryption(temp_matrix))



    else:
        if len(message_hex) % 16 != 0:
            cipher_padding = 16 - (len(message_hex) % 16)
            for _ in range(cipher_padding):
                message_hex.append(hex(ord(' ')))

        loop_count = int(len(message_hex) / 16)

        for i in range(loop_count):
            temp_matrix = StateMatrixGeneration(message_hex[i * 16: (i + 1) * 16])

            state_matrix.append(AES_encryption(temp_matrix))

    return state_matrix


def DecryptMessage(encrypted_msg):
    global key_matrix, num_rounds
    decrypted_msg = []

    for i in range(len(encrypted_msg)):
        decrypted_msg.append(AES_decryption(encrypted_msg[i]))

    return decrypted_msg


# ============================= W generation ==========================


def W_generation(K, rcon):
    W = []
    for i in range(4 * (num_rounds)):
        if i < key_word_len:
            W.append(K[i])
        elif i >= key_word_len and i % key_word_len == 0:
            # print("inside second cond")
            temp = W[i - 1]
            temp = temp[1:] + [temp[0]]

            for j in range(len(temp)):
                # b = BitVector(hexstring = temp[j])
                # int_val = b.intValue()

                int_val = int(temp[j], 16)
                s = Sbox[int_val]

                # s = BitVector(intVal=s, size=8)
                # temp[j] = s.get_bitvector_in_hex()
                temp[j] = hex(s)

            temp2 = []
            for j in range(len(temp)):
                temp2.append(
                    hex(int(W[i - key_word_len][j], 16) ^ int(temp[j], 16) ^ int(rcon[int(i / key_word_len) - 1][j],
                                                                                 16)))

            W.append(temp2)


        elif i >= key_word_len and key_word_len > 6 and i % key_word_len == 4:
            # print("inside third cond")
            temp = W[i - 1]

            for j in range(len(temp)):
                int_val = int(temp[j], 16)
                s = Sbox[int_val]
                temp[j] = hex(s)

            temp2 = []
            for j in range(len(temp)):
                temp2.append(hex(int(W[i - key_word_len][j], 16) ^ int(temp[j], 16)))

            W.append(temp2)

        else:
            # print("inside else")
            temp = W[i - 1]
            temp2 = []
            for j in range(len(temp)):
                temp2.append(hex(int(W[i - key_word_len][j], 16) ^ int(temp[j], 16)))

            W.append(temp2)

    return W

    # for()

    # print("after calculating W ")
    # print("size of W, ", len(W))
    # print(W)

    # for i in range(0, len(W), 4):
    #     print('round {} keys: {} {} {} {}'.format(i/4, W[i], W[i+1], W[i+2], W[i+3]))
    # print("round 0: ", W[i], W[i+1], W[i+2], W[i+3])


# =================================== Key Matrix Generation: ===============================

def Key_matrix_generation(W):
    # key_matrix = []

    global key_matrix

    for i in range(int(len(W) / 4)):
        temp = W[i * 4: (i + 1) * 4]
        temp2 = [[0, 0, 0, 0] for _ in range(4)]

        for j in range(4):
            for k in range(4):
                temp2[k][j] = temp[j][k]
        key_matrix.append(temp2)

    # print("state matrix: ")
    # print(state_matrix)
    # print("key matrix : ")
    # print(key_matrix)
    # print("key matrix size: ", len(key_matrix))


def AES_handler(input_key):
    global key_word_len, num_rounds, rcon_num, rcon, key_scheduling_time

    print("1. AES-128")
    print("2. AES-192")
    print("3. AES-256")

    choice = int(input("Enter choice: "))

    key_word_len = 4
    num_rounds = 11
    rcon_num = 10
    rcon = []

    if choice == 2:
        key_word_len = 6
        num_rounds = 13
        rcon_num = 8
    elif choice == 3:
        key_word_len = 8
        num_rounds = 15
        rcon_num = 7

    key_hex = []
    for ch in input_key:
        key_hex.append(hex(ord(ch)))

    if len(key_hex) > key_word_len * 4:
        key_hex = key_hex[:key_word_len * 4]
    elif len(key_hex) < key_word_len * 4:
        current_len = len(key_hex)
        for _ in range(key_word_len * 4 - current_len):
            ch = ' '
            key_hex.append(hex(ord(ch)))

    # print("After padding key_hex: ", key_hex)

    # generating K
    time_start = time.time()

    K = []
    for i in range(key_word_len):
        K.append(key_hex[i * 4: (i + 1) * 4])

    # print("this is K: ")
    # print(K)

    # generating rcon:
    rcon = rcon_calc(rcon_num)

    # generating W matrix:
    W = W_generation(K, rcon)
    key_scheduling_time = time.time() - time_start

    # key_scheduling_time = key_scheduling_time/(10**9)

    # generating Round key matrix
    Key_matrix_generation(W)


# ======================================= Bonus ======================================

def EncryptFile(fileDir):
    # global AES_input, pad_count_input, input_filename

    global padded_count

    # input_filename = input("Enter filename (inside ./res/): ")

    myFile = open("./input_files/{}".format(fileDir), "rb")
    file_hex = bytes.hex(myFile.read())
    myFile.close()

    print("file bytes hex")
    # print(file_hex)
    print(len(file_hex))
    # print(file_hex)


    if (len(file_hex) % 32) != 0:
        padded_count = 32 - len(file_hex) % 32
        file_hex = file_hex + '0' * padded_count
        # pad_count_input = 32 - len(file_content) % 32
        # file_content = file_content + "0" * pad_count_input

    # AES_input += BitVector(hexstring=file_hex)


    print("file bytes hex")
    # print(file_hex)
    print(len(file_hex))

    print("padded_count : ", padded_count)

    # print(file_hex)


    text_str = ''
    for i in range(0, len(file_hex)-1, 2):
        # print(file_hex[i: i+2], i)
        bv = BitVector(hexstring=file_hex[i: i+2])
        ascii_ch = bv.get_bitvector_in_ascii()
        # print(ascii_ch, i)
        text_str += ascii_ch

    print("=================================================================")
    # print(text_str)
    print(file_hex)

    encrypted = EncryptMessage(text_str)
    print("===================================================================")
    print("===================================================================")
    print("===================================================================")
    print(" Encrypted" )
    print(encrypted)

    return encrypted


def DecryptFile(encrypted_file, fileName):
    # global decipher_output

    global padded_count

    decrypted_file = DecryptMessage(encrypted_file)
    print("===================================================================")
    print("===================================================================")
    print("===================================================================")
    print(" Decrypted")

    print(decrypted_file)

    printable_file = []
    for i in range(len(decrypted_file)):
        chunk = decrypted_file[i]
        for j in range(4):
            for k in range(4):
                # ch = chr(int(chunk[k][j], 16))

                hexVal_bv = BitVector(intVal=int(chunk[k][j], 16), size=8)

                # print(chunk[k][j], int(chunk[k][j], 16))
                # hexVal = hexVal_bv.get_bitvector_in_hex()
                # printable_file += hexVal
                # printable_file += chunk[k][j]
                printable_file.append(ord(hexVal_bv.get_bitvector_in_ascii()))


    # print(printable_file)

    printable_file = bytearray(printable_file[:-padded_count])
    immutable_bytes = bytes(printable_file)

    # decrypted_file_str = print_message(decrypted_file)

    print(printable_file)

    file = open("./output_files/{}".format(fileName), "wb")
    # print(plain_arr)
    # bytes = b"0x410x420x43"
    file.write(immutable_bytes)
    file.close()




    # file_obj = open("./output_files/{}".format(fileName), "wb+")
    # file_obj.write(bytes.fromhex(
    #     printable_file[: len(printable_file) - padded_count]))
    # file_obj.close()

    # file_obj.write(bytes.fromhex(
    #     decipher_output.get_bitvector_in_hex()[: len(decipher_output.get_bitvector_in_hex()) - padded_count]))
    # file.close()


# ===================================== Input Encryption ===================================
# =====================================   AES   ============================================
# provide num_rounds = 11 for AES-128
#                    = 13 for AES-192
#                    = 15 for AES-224


def main():

    global key_scheduling_time, encryption_time, decryption_time

    input_key = input("input AES key: ")

    AES_handler(input_key)

    print("1. Input Plain Text: ")
    print("2. Input File")

    option = input("Enter choice: ")

    if int(option) == 1:
        input_message = input("Enter Plain Text: ")

        print("Plain text:")
        print(input_message)
        print_hex(input_message)

        print("\nKey: ")
        print(input_key)
        print_hex(input_key)

        time_start = time.time()
        encrypted_msg = EncryptMessage(input_message)
        encryption_time = time.time() - time_start
        print("\nCipher text: ")
        print_cipher_hex(encrypted_msg)
        print_message(encrypted_msg)

        time_start = time.time()
        decrypted_msg = DecryptMessage(encrypted_msg)
        decryption_time = time.time() - time_start

        print("Deciphered Text: ")
        print_cipher_hex(decrypted_msg)
        print_message(decrypted_msg)


    elif int(option) == 2:
        fileDir = input("Enter filename: ")

        time_start = time.time()
        encrypted_file = EncryptFile(fileDir)
        encryption_time = time.time() - time_start

        time_start = time.time()
        DecryptFile(encrypted_file, fileDir)
        decryption_time = time.time() - time_start

    else:
        print("Unknown Command")


    print("\nExecution Time: ")
    print("Key Scheduling: {}".format(key_scheduling_time))
    print("Encryption Time: {}".format(encryption_time))
    print("Decryption Time: {}".format(decryption_time))


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()

# receive data from the server and decoding to get the string.
# print (s.recv(1024).decode())
# close the connection
# s.close()
