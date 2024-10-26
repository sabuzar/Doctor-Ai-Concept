import csv

appending_data = [
    'questions','answers'
]
storing_file = open(f'chapter1.csv', 'a', newline="",encoding ="utf-8")
writer = csv.writer(storing_file)
writer.writerow(appending_data)
storing_file.close()