Level 0 (Root):
Merkle Root Hash: 0123456789abcdef

Level 1:
Hash01 (Hash of Data1 + Data2): 01aabbccddeeff00
Hash23 (Hash of Data3 + Data4): 11aabbccddeeff11
Hash45 (Hash of Data5 + Data6): 21aabbccddeeff22
Hash67 (Hash of Data7 + Data8): 31aabbccddeeff33
Hash89 (Hash of Data9 + Data10): 41aabbccddeeff44
Hash1011 (Hash of Data11 + Data12): 51aabbccddeeff55
Hash1314 (Hash of Data13 + Data14): 61aabbccddeeff66
Hash1516 (Hash of Data15 + Data16): 71aabbccddeeff77
Hash1718 (Hash of Data17 + Data18): 81aabbccddeeff88
Hash1920 (Hash of Data19 + Data20): 91aabbccddeeff99
Hash2122 (Hash of Data21 + Data22): a1aabbccddeeffaa
Hash2324 (Hash of Data23 + Data24): b1aabbccddeeffbb
Hash2526 (Hash of Data25 + Data26): c1aabbccddeeffcc
Hash2728 (Hash of Data27 + Data28): d1aabbccddeeffdd
Hash2930 (Hash of Data29 + Data30): e1aabbccddeeffee

Level 2:
Hash0123 (Hash of Hash01 + Hash23): f1aabbccddeeffff
Hash4565 (Hash of Hash45 + Hash65): f2aabbccddeeffaa
Hash7879 (Hash of Hash67 + Hash89): f3aabbccddeeffbb
Hash101112 (Hash of Hash1011 + Hash1314): f4aabbccddeeffcc
Hash151617 (Hash of Hash1516 + Hash1718): f5aabbccddeeffdd
Hash192021 (Hash of Hash1920 + Hash2122): f6aabbccddeeffee
Hash232425 (Hash of Hash2324 + Hash2526): f7aabbccddeeffff
Hash272829 (Hash of Hash2728 + Hash2930): f8aabbccddeeffaa

Level 3:
Hash01234567 (Hash of Hash0123 + Hash4565): f9aabbccddeeffbb
Hash78791011 (Hash of Hash7879 + Hash101112): faaabbccddeeffcc
Hash15161718 (Hash of Hash151617 + Hash192021): fbaabbccddeeffdd
Hash23242526 (Hash of Hash232425 + Hash272829): fcaabbccddeeffee

Level 4 (Root):
Merkle Root Hash: fdaabbccddeeffff

Each hash in a Merkle Tree can contain 83 bytes of data, 
this allows for the use of a large variety of applications
on the chain such as game or dapps. 30 hashes as shown above
from Root hash reconstruction can host up to 28/29/30 x 83 bytes
of data, we can use CBOR/Hex on SVG images to inscribe them to a
Merkle Tree that can be loaded by a front end loaded by calling
the Merkle Tree, any change in any Hash when reforming the data
will result in a different Root hash. Essentially making the only
way to get X from Y is by following the Merkle Root Hash tree. 

There is no limit of leaf levels and nodes. The only limit is BLOCK SIZE.

100ln x 83b = 8.3 KB 
200ln x 83b = 16.6 KB
