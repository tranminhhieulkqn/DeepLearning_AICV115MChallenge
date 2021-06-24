import csv, os

covid_files = os.listdir('../covid')
non_covid_files = os.listdir('../non_covid')

#print(covid_files)
#print(non_covid_files)

with open('../cough_dataset.csv', mode='w') as cough_subset:
    cough_subset_writer = csv.writer(cough_subset, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for file in covid_files:
        cough_subset_writer.writerow([file, 'covid'])

    for file in non_covid_files:
        cough_subset_writer.writerow([file, 'not_covid'])
