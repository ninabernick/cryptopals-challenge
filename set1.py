
import base64
import sys


def hex_to_base64(s):
    byte_sequence = bytes.fromhex(s)
    bin_string = ''
    b64_index_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    for byte in byte_sequence:
        bin_string += (bin(byte)[2:].zfill(8)) 
    ans = ''
    print(bin_string)

    for i in range(0, len(bin_string), 6):
        piece = bin_string[i:i+6]
        print(piece)
        if len(piece) == 2:
            if '1' in piece:
                piece += '0000'
                ans += b64_index_table[int(piece, 2)]
            else:
                ans += '=='
        elif len(piece) == 4:
            if '1' in piece:
                piece += '00'
                ans += b64_index_table[int(piece,2)]
            else:
                ans += '='
        else:
            ans += b64_index_table[int(piece, 2)]

    print(ans)

def xor_fixed(s1, s2):
    s1 = bytes.fromhex(s1)
    s2 = bytes.fromhex(s2)
    joined = zip(s1, s2)
    byte_string = bytearray()
    for b1, b2 in joined:
        print(bin(b1))
        print(bin(b2))
        print(bin(b1^b2))
        byte_string.append(b1^b2)
    return byte_string.hex()

def english_score(s, english_dict):
    total = 0
    for char in s:
        total += english_frequencies[char]
    return total/len(s)

#XOR-ing twice gives you your original string back
def single_byte_xor(bytestring, char):
    output = bytearray()
    for byte in bytestring:
        output.append(byte ^ char)
    return output

def get_english_score(bytestring):
    english_frequencies = {
        'a': .08497,
        'b': .01492,
        'c': .02202,
        'd': .04253,
        'e': .11162,
        'f': .02228,
        'g': .02015,
        'h': .06094,
        'i': .07546,
        'j': .00153,
        'k': .01292,
        'l': .04025,
        'm': .02406,
        'n': .06749,
        'o': .07507,
        'p': .01929,
        'q': .00095,
        'r': .07587,
        's': .06327,
        't': .09356,
        'u': .02758,
        'v': .00978,
        'w': .0256,
        'x': .0015,
        'y': .01994,
        'z': .00077,

    }
    score = 0

    for char in english_frequencies:
        try:
            instances = bytestring.decode().count(char)
            freq = instances/len(bytestring)
            diff = 1 - abs(freq - english_frequencies[char])
            score += diff
        except UnicodeDecodeError:
            continue

    return score

def decode_xor_string(byte_string):
    maxscore = 0
    best = ''
    for i in range(256):
        output = single_byte_xor(byte_string, i)
        score = get_english_score(output)
        if (score  > maxscore):
            maxscore = score
            best = output

    return (best, maxscore)

def find_xored_string(fp):
    f = open(fp)
    lines = f.readlines()
    maxscore = 0
    best = ''
    for line in lines:
        (decoded, score) = decode_xor_string(bytes.fromhex(line))
        if score > maxscore:
            maxscore = score
            best = decoded
        #print(decoded, score)

    return (best, maxscore)


def main():
    """Launcher."""
    print(find_xored_string('xor_strings.txt')[0].decode())
 
if __name__ == "__main__":
    main()



#filepath = 'xor_strings.txt'
#find_xored_string(filepath)
#xor_fixed('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965')
