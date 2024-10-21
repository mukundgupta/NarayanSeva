import csv

item = input("Item Delivered: ")
units = int(input("Number of units of items delivered: "))

def remove_items(item, units):
    l = []
    with open("item_detail.csv", "r+",newline='') as file:
        
        reader = csv.reader(file)
        found = False
        #iterating over each row
        for row in reader:
            # checking if item is in inventory
            if row[0] == item:
                print(f"{units} units of item {item} were removed")
                rem = int(row[2])-units
                found = True
                if rem >= 1:
                    #add row to list
                    l.append([item,row[1], rem])
                else:
                    print("all units of items removed.")

            else:
                l.append(row)
        if found == False:
            print("Item not found in inventory!")

        file.seek(0)
        writer = csv.writer(file)
        writer.writerows(l)

     
remove_items(item, units)


