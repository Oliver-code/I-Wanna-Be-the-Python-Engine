massive_string = """FF000000
FF2c2c2c
FF606060
FFc8c0c0
FF004058
FF008894
FF01e8e4
FF01f8fc
FF005800
FF00a848
FF58f89c
FFb0f0d8
FF006800
FF00a800
FF58d858
FFb8f878
FF007800
FF00b800
FFbcf818
FFdcf878
FF503000
FFac8000
FFfcb800
FFfcd884
FF8c1800
FFe46018
FFfca048
FFfce0b4
FFac1000
FFfc3800
FFfc7858
FFf4d0b4
FFac0028
FFe40060
FFfc589c
FFf4c0e0
FF94008c
FFdc00d4
FFfc78fc
FFfcb8fc
FF4028c4
FF6848fc
FF9c78fc
FFdcb8fc
FF0000c4
FF0088fc
FF6888fc
FFbcb8fc
FF0000fc
FF0078fc
FF38c0fc
FFa4e8fc
FF788084
FFbcc0c4
FFfcf8fc
FF22123b
FF360900
FF9e9e5c
"""

new_string = ""
count = 0
for letter in massive_string:
    if letter != "\n"  and letter != "F":

        new_string += letter
        if count == 5:
            new_string += ","
        count += 1
        count = count % 6
print(new_string)