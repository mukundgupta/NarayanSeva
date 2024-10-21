import csv as c
def de_if_exp():
    f = open('item_detail.csv','r')
    r = c.reader(f)

    inven = open("inventory.txt", "r")
    inv = int(inven.read()) #put actual inventory here

    l = []
    next(r)

    for i in r:
        
        if int(i[1])-1 > 0 : #as we are checking expiry for next day to put in inventory
            l.append(i)
        else:
            inv-=(int(i[2]))
        

    f1 = open('item_detail.csv','w',newline = '')
    w = c.writer(f1)
    w.writerow(['Packaged item name','Days till expiry','Units'])
    w.writerows(l)# file with item that will be expired tomorrow removed
    f1.close()
    with open("inventory.txt","w") as file:
        file.write(str(inv))

    print(inv)
    

