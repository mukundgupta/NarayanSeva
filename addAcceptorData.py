import csv
import get_coord_display

'''Takes a list with donor data as argument. 
Generates an ID, attempts to get coordinates(latitude, longitude) from the provided address using get_coord_display.py and then appends data to a CSV file (donorData.csv)'''

#Structure of donor data:
#["donor_id","name_of_org", "contact","email","address","coordinates"]
def get_id():
    '''returns the new ID that is to be appended.'''
    with open("static/acceptorData.csv", "r",newline='') as file:
        reader = csv.reader(file)
        
        count = 0
        for row in reader:
            count += 1
    print("ROWS: ", count)
    return count
        
def add_acceptor_data(a_data):
    '''appends donor data to a csv file.'''
    with open("static/acceptorData.csv", "a+",newline='\n') as file:

        writer = csv.writer(file)
        count = get_id()
        
        name = a_data[0]
        num = a_data[1]
        email = a_data[2]
        addr = a_data[3]
        req =a_data[4]
        coords = get_coord_display.get_coordinates(addr)
        
        writer.writerow([count, name, num, email, addr, req,coords])

    return "Done"
    
    

