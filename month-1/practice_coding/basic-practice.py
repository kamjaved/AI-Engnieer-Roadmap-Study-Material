# ---------EXTRAS PRACTICE REFRESHERS---------


# num_1= input ("Please enter you 1st number: ")
# num_2= input ('Please enter your 2nd number:  ')

# print ('Your total sum is: ', int(num_1) + int (num_2))
print("value".replace("e", "3"))


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(numbers[7:0:-2])

if 2 > 4:
    print("correct result")
elif 4 > 2:
    print("correct result again")
    if len([1, 2, 3]) > 2:
        print("list is long enough")
else:
    print("Incorrect result")

if 2 > 4:
    print("correct result--")
elif 4 > 2:
    print("correct details--")
    if len([4, 3, 2, 1]) > 2:
        print("correct again----")
else:
    print("Incorrect details--")


def shouter(text, times=2):
    counter = 1
    while counter <= times:
        if times >= 10:
            print("You are too loud")
            break
        else:
            print(text.upper())
            counter += 1

    return "DONE"


status = shouter("hello john greetings", 9)
print(status)

# For Loop over a list
models = ["gpt-4", "gpt-4o", "gemini"]
for m in models:
    print(f"Supported: {m}")

user_name = "john"
age = 24

good_approach = f"{user_name} is {age + 10} year old"
print(good_approach.capitalize())

# To capitalize the whole sentence, use .upper() instead of .capitalize()
# .capitalize() only capitalizes the first character
# .upper() converts all characters to uppercase
print(good_approach.upper())

# # For Loop over a Dictionary (Items gives both Key and Value)
# for model_name, rate in pricing_per_1m.items():
#     print(f"{model_name} costs ${rate}")
