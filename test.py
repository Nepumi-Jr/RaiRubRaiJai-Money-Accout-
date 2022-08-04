x = 3
print(x)
x = x + 1
#! ถ้าปิด x จะหาย
with open("data.txt", "w") as f:
    f.write(str(x))
# ? File system
