from extractor import Extractor


# Path to directory.
# The directory should have a folder with all the csv files named "datasets" 
PATH_TO_DATA = r"G:\My Drive\Road to 10K"

extract = Extractor(PATH_TO_DATA)

message = 'What would you like to do?\n\t1. Plot graphs\n\t2. Plot and save graphs\n\t3. Add VO2 data\n\t4. Proccess new data\n\t5. Define tracking values (Not implemented yet)\n\t6. Quit\n'

print('Welcome to the running data extractor!')
selection = "0"
selection = input(message)
while selection != "6":
    if selection not in [str(i) for i in range(1,6)]:
        print('You have input incorrectly. Try again')
        selection = input()
    elif selection == "1":
        extract.plot()
    elif selection == "2":
        extract.plot_and_save()
    elif selection == "3":
        extract.add_VO2()
    elif selection == "4":
        if extract.track == []:
            print('No tracking values selected (only default implemented)')
            extract.define_tracking()
        extract.process()
    elif selection == '5':
        print('Not implemented yet')
    
    selection = input(message)

extract.save_data()
print('Goodbye!')