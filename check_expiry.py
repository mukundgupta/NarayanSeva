<<<<<<< HEAD
items = {"store1":{'item 1':[30,3],'item 2':[60,4]},"store2":{'item 1':[40,7],'item 2':[60,4] }}

to_notify = {}

for store in items:
    print(store)
    for item in items[store]:
        print(items[store][item])
        if items[store][item][1] <= 5:
            to_notify[store] = True
        
for i in to_notify:
    print(i)
=======
items = {"store1":{'item 1':[30,3],'item 2':[60,4]},"store2":{'item 1':[40,7],'item 2':[60,4] }}

to_notify = {}

for store in items:
    print(store)
    for item in items[store]:
        print(items[store][item])
        if items[store][item][1] <= 5:
            to_notify[store] = True
        
for i in to_notify:
    print(i)
>>>>>>> 45147a1f7bb4677053e53e813b6840f86ae203de
