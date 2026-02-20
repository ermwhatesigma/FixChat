import csv

print("Select how many api you want:")
count = int(input("> "))

print(f"You selected {count} different API\n")

keys = []

for i in range(1, count + 1):
    key = input(f"API {i}: ")
    print(f"API {i} = {key}\n")
    keys.append(key)

with open("OpenAI_API.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Index", "API_Key"])
    for i, key in enumerate(keys, start=1):
        writer.writerow([i, key])

print("API keys saved in OpenAI_API.csv")