#first load all the file names from the folder (list of strings)
#We need a stack the size of the number of threads in CPU

#1. Fill the stach with file handlers
#2. Invoke threads for each stack element and process...
#3. Once the thread is done, pop the stack and load the new file.
#4. Refill the stack
#5. GO TO 2 until the stack is empty

#Processing alg:
#   Get rid of rows without location
#   Sort each file by start date
#   Split result by QUARTER into another file like 2017Q1.csv

#split files (96).csv -> sorted (96) -> split-by-quarter(20).csv -> sorted-and-split(20).csv
