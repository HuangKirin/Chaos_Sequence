import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# 定义非线性混沌映射的动力方程
def logistic_map(x, alpha, beta):
    term1 = (1 - beta ** -4) * (1 / math.tan(alpha / (1 + beta)))
    term2 = (1 + 1 / beta) ** beta
    term3 = math.tan(alpha * x)
    term4 = (1 - x) ** beta
    term = term1 * term2 * term3 * term4
    return term


# 混沌序列生成函数
def generate_chaos_sequence(seed, alpha, beta, n):
    chaos_sequence = [seed]
    for i in range(1, n):
        next_value = logistic_map(chaos_sequence[-1], alpha, beta)
        chaos_sequence.append(next_value)
    return chaos_sequence


# 加密函数
def encrypt(text, alpha, beta):
    encrypted_text = ""
    chaos_sequence = generate_chaos_sequence(0.666, alpha, beta, len(text) * 3)
    pl = []
    en_ = []
    for i in range(0, len(text), 3):
        current_char = text[i:i + 3]
        encrypted_char = ""
        for k in range(len(current_char)):
            chaos_value = chaos_sequence[i + k] * 2 ** 256
            byte = ord(current_char[k])
            pl.append(byte)
            encrypted_byte = byte ^ int(math.fmod(chaos_value, 2 ** 256))
            en_.append(encrypted_byte)
            encrypted_char += (" " if k > 0 else "") + str(encrypted_byte)
        encrypted_text += (" " if i > 0 else "") + encrypted_char

    return encrypted_text, pl, chaos_sequence, en_


# 解密函数
def decrypt(encrypted_text, alpha, beta):
    decrypted_text = ""
    chaos_sequence = generate_chaos_sequence(0.666, alpha, beta, len(encrypted_text.split()))

    for encrypted_byte_str in encrypted_text.split():
        encrypted_byte = int(encrypted_byte_str)
        chaos_value = chaos_sequence.pop(0) * 2 ** 256
        decrypted_byte = encrypted_byte ^ int(math.fmod(chaos_value, 2 ** 256))
        decrypted_text += chr(decrypted_byte)

    return decrypted_text


# 明文
plaintext = "台湾是中国的台湾。中华民族的历史、文化和两岸关系发展的历程充分证明：海峡的距离，阻隔不断两岸同胞的骨肉亲情。制度的不同，改变不了两岸同属一个国家、一个民族的客观事实。外部的干涉，阻挡不了家国团圆的历史大势。"
print(len(plaintext))
# 加密过程
start_time = time.time()
encrypted_text, pl, chaos, en_b = encrypt(plaintext, 0.7, 28.0)

fig, axs = plt.subplots(3, 1)


def update(i):
    axs[0].clear()
    axs[0].plot(pl[:i])
    axs[0].set_title('PlainText')
    axs[1].clear()
    axs[1].plot(chaos[:3 * i])
    axs[1].set_title('ChaosSequence')
    axs[2].clear()
    axs[2].plot(en_b[:i])
    axs[2].set_title('EncryptText')
    return axs,


ani = FuncAnimation(fig, update, frames=None, interval=100)
plt.subplots_adjust(wspace=0.5, hspace=0.5)
plt.show()

end_time = time.time()
print(len(encrypted_text))
print("加密后:", encrypted_text)

# 计算加密时间
encryption_time = end_time - start_time
print("加密函数执行时间:", encryption_time * 1000, "毫秒")

# 解密过程
start_time = time.time()
decrypted_text = decrypt(encrypted_text, 0.7, 28.0)
end_time = time.time()
print(len(decrypted_text))
print("解密后:", decrypted_text)

# 计算解密时间
decryption_time = end_time - start_time
print("解密函数执行时间:", decryption_time * 1000, "毫秒")
