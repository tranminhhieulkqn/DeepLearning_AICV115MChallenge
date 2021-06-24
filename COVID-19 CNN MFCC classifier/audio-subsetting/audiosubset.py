import os, csv, subprocess
from sklearn.model_selection import train_test_split

class Audiosubset():
    def __init__(self):
        pass

    def create_subset_csv(self):
        datasets = ['./balanced_train_segments.csv', './unbalanced_train_segments_no_quotes.csv', './eval_segments.csv']
        cough_dataset = []

        for dataset in datasets:
            with open(dataset) as eval_segments:
                csv_reader = csv.reader(eval_segments, delimiter=',')
                line_count = 0
                not_found = 0
                row_count = 0

                for row in csv_reader:
                    if row[0].startswith('#'):
                        print(row[0])
                    else:
                        if any("/m/01b_21" in s for s in row):
                            cough_dataset.append(row)

        # Write out the CSV
        print('Cough rows: ', len(cough_dataset))

        # Write out the CSV
        output_csv = './cough_subset.csv'
        if os.path.exists(output_csv):
            os.remove(output_csv)

        with open(output_csv, mode='w') as cough_subset:
            cough_subset_writer = csv.writer(cough_subset, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in cough_dataset:
                cough_subset_writer.writerow(row)

    def replace_element(self, list, label):
        return [x if label in list else list for x in list]

    def download_subset(self):
        with open('./cough_subset.csv') as download:
            csv_reader = csv.reader(download, delimiter=',')
            for row in csv_reader:
                filename = row[0]+'_'+row[1]+'_'+row[2]
                if not os.path.isfile("../non_covid/"+filename+".wav"):
                    print("Downloading...", row[1])
                    subprocess.check_call(['./download.sh', row[0], row[1], row[2]])
                else:
                    print(filename)
                    print("Got it!")

    def validate_download_subset(self):
        output_csv_final = './cough_subset_final.csv'
        output_csv = './cough_subset.csv'

        if os.path.exists(output_csv_final):
            os.remove(output_csv_final)

        with open(output_csv) as download:
            csv_reader = csv.reader(download, delimiter=',')

            with open(output_csv_final, mode='w') as cough_subset:
                cough_subset_writer = csv.writer(cough_subset, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                dropped = 0
                kept = 0
                for row in csv_reader:
                    if os.path.exists('../non_covid/'+row[0]+'_'+row[1]+'_'+row[2]+'.wav'):
                        # Download successful add to the final metadata CSV
                        cough_subset_writer.writerow(row)
                        kept += 1
                    else:
                        dropped += 1

        print("Kept", kept)
        print("Dropped", dropped)

    def split_dataset_train_test(self):
        master_dataset = []
        with open('./cough_subset_final.csv') as cough_subset:
            csv_reader = csv.reader(cough_subset, delimiter=',')
            for row in csv_reader:
                master_dataset.append(row)

        master_length = len(master_dataset)
        train_length = (master_length/100)*80
        test_length = (master_length/100)*20

        X_train = []
        X_test = []
        index = 0
        for training_data in master_dataset:
            if index < train_length:
                X_train.append(training_data)
                index += 1
            else:
                X_test.append(training_data)

        print("Train length", len(X_train))
        print("Test length", len(X_test))

        # Write the training dataset
        train_path = './cough_subset_train.csv'
        if os.path.exists(train_path):
            os.remove(train_path)

        with open(train_path, mode='w') as cough_subset_train:
            cough_subset_writer = csv.writer(cough_subset_train, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in X_train:
                cough_subset_writer.writerow(row)

        # Write the test dataset
        test_path = './cough_subset_test.csv'
        if os.path.exists(test_path):
            os.remove(test_path)

        with open(test_path, mode='w') as cough_subset_test:
            cough_subset_writer = csv.writer(cough_subset_test, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in X_test:
                cough_subset_writer.writerow(row)

subset = Audiosubset()
#subset.create_subset_csv()
#subset.download_subset()
subset.validate_download_subset()
#subset.split_dataset_train_test()
