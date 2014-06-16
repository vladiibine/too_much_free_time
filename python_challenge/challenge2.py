import string

ord_a = ord('a')
ord_z = ord('z')
ord_A = ord('A')
ord_Z = ord('Z')

secret = ("g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc "
          "dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr "
          "gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml "
          "rfc spj.")

from_small = ''.join(
    [chr(elem) for elem in range(ord_a, ord_z + 1)]
)

to_small = ''.join(
    [chr(ord(elem) + 2 + (0 if elem in from_small[2:] else ord_z - ord_a))
     for elem in from_small]
)

# print from_small
# print to_small
trans = string.maketrans(from_small, to_small)
translated_string = string.translate(secret, trans)

print translated_string