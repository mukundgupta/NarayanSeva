import csv

def remove_if_expired():
    l = []
    with open("item_detail.csv","r") as file:
        reader = csv.reader(file)
        inv = open("inventory.txt", "r")
        inventory = int(inv.read())
        inv.close()

        waste = 0
        l = []
        for row in reader:
            if (int(row[1]-1)) > 0:
                l.append(row)
            else:
                inventory -= int(row[2])
                waste += int(row[2])

    with open("item_detail.csv","a+") as file:
        file.seek(0)
        reader = csv.reader(file)
        next(reader)
        file.truncate()
        writer = csv.writer(file)
        writer.writerows(l)
    
    print(f"food expired:{waste}\nfood in inventory after removal: {inventory}")

    with open("inventory.txt", "w") as file:
        file.write(str(inventory))

remove_if_expired()
        