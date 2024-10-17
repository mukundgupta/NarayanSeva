items = {"store1":{'item 1':[30,3],'item 2':[60,4]},"store2":{'item 1':[40,7],'item 2':[60,4] }}

to_notify = {}

for store in items:
    print(store)
    for item in items[store]:
        print(items[store][item])
        
for i in to_notify:
    print(i)
