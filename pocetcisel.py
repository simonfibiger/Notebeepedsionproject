number_count = int(input("zadej pocet cisel: "))
numbers = []
for number in range(number_count):
    number = int(input(f"zadej {number + 1}. cislo: "))
    numbers.append(number)  


print(f"zadal jsi: {', '.join(str(n) for n in numbers)}")
print(f"odzadu: {', '.join(str(n) for n in reversed(numbers))}")
print(f"nejvetsi cislo: {max(numbers)}")
print(f"nejmensi cislo: {min(numbers)}") 