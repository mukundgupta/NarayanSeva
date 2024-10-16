import csv
import get_coord_display


#Structure of donor data:
#["donor_id","name_of_org", "contact","email","address","coordinates"]
def get_id():
    with open("donorData.csv", "r",newline='') as file:
        reader = csv.reader(file)
        
        count = 0
        for row in reader:
            count += 1
    print("ROWS: ", count)
    return count
        
def add_donor_data(d_data):
    
    with open("donorData.csv", "a+",newline='\n') as file:

        writer = csv.writer(file)
        count = get_id()
        
        name = d_data[0]
        num = d_data[1]
        email = d_data[2]
        addr = d_data[3]
        coords = get_coord_display.get_coordinates(addr)
        
        writer.writerow([count, name, num, email, addr, coords])

    return "Done"
    
    

