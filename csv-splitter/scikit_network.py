import pandas
from pandas.plotting import scatter_matrix
from pandas.plotting import andrews_curves
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import csv
from datetime import datetime


class Program:
    url = "C:/Users/rajmu/Desktop/project-4/crimes_ML_ready_new.csv"
    validation_size = -1
    seed = -1

    def __init__(self, test_size, seed):
        print('Loading dataset...')
        self.test_size = test_size
        self.network_seed = seed
        self.dataset = pandas.read_csv(Program.url, sep=';', low_memory=False)
        print('Dataset loadded. Formatting...')
        cols = list()
        cols = self.dataset.columns.values.tolist()
        cols = cols[:12] + cols[32:] + cols[13:32]
        self.dataset = self.dataset[cols]
        for col in cols:
            col.replace('`', ' ')

        
        self.dataset.columns = cols

        self.dataset['Date'] = self.dataset['Date'].str[:10]
        self.dataset['Date'] = self.dataset['Date'].str.replace('-','')
        self.dataset["Date"] = self.dataset['Date'].astype('int64')
        del self.dataset["Latitude"] #= self.dataset['Latitude'].str.replace(',','.')
        del self.dataset["Longitude"] #= self.dataset['Longitude'].str.replace(',','.')
        #self.dataset["Latitude"] = self.dataset['Latitude'].astype('float64')
        #self.dataset["Longitude"] = self.dataset['Longitude'].astype('float64')
        print(len(self.dataset.axes[0]))
        self.dataset = self.dataset.dropna()
        print(len(self.dataset.axes[0]))
        print('Dataset initialized successfully!')

    def info(self):
        print(self.dataset.shape)
        print(self.dataset.describe())

    def show_sample(self, amt=10):
        print(self.dataset.head(amt))

    def show_whisker_plots(self):
        self.dataset.plot(kind="box", subplots=True, layout=(1, 4), sharex=False, sharey=False)
        plt.show()

    def show_histogram(self):
        # histograms
        self.dataset.hist()
        plt.show()

    def show_matrix(self):
        scatter_matrix(self.dataset)
        plt.show()

    def show_curves(self):
        andrews_curves(self.dataset, 'class')
        plt.show()

    def __split_validation_dataset(self):
        array = self.dataset.values
        X = array[:, :39]
        Y = array[:, 39:]
        Program.validation_size = 0.00001
        Program.seed = 12
        return model_selection.train_test_split(X, Y, test_size=self.test_size, random_state=self.network_seed)

    def test_models(self):
        X_train, X_validation, Y_train, Y_validation = Program.__split_validation_dataset(self)
        scoring = 'accuracy'
        models = []
        models.append(('LR', LogisticRegression()))
        models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVM', SVC()))
        # evaluate each model in turn
        results = []
        names = []
        for name, model in models:
            kfold = model_selection.KFold(n_splits=10, random_state=Program.seed)
            cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)
        # visualize test data
        fig = plt.figure()
        fig.suptitle('Alg comparison')
        ax = fig.add_subplot(111)
        plt.boxplot(results)
        ax.set_xticklabels(names)
        plt.show()

    def predict_with_knn(self):
        print('Starting KNN prediction model...')
        knn = KNeighborsClassifier()
        x_train, x_validation, y_train, y_validation = Program.__split_validation_dataset(self)
        knn.fit(x_train, y_train)
        print('Model initialized. Predicting...')
        predictions = knn.predict(x_validation)
        accuracy = accuracy_score(y_validation, predictions)
        print('Prediction complete!')
        #print(confusion_matrix(y_validation, predictions))
        print(classification_report(y_validation, predictions))
        return accuracy, self.test_size, 'KNeighborsClassifier'


    def predict_with_decision_tree(self):
        print('Starting Decision Tree prediction model...')
        dt = DecisionTreeClassifier()
        x_train, x_validation, y_train, y_validation = Program.__split_validation_dataset(self)
        dt.fit(x_train, y_train)
        prediction = dt.predict(x_validation)
        accuracy = accuracy_score(y_validation, prediction)
        print('Prediction complete!')
        print(classification_report(y_validation, prediction))
        return accuracy, self.test_size, 'DecisionTreeClassifier'


def main():
    p = Program(0.2, 7)
    print(p.dataset.describe())
    
    test_sizes = [0.9, 0.8, 0.5, 0.4, 0.2, 0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
    results = list()
    for size in test_sizes:
        p.test_size = size
        acc, ts, cls = p.predict_with_decision_tree()
        results.append('[{}] f1: {}; test size: {}; method: {}'.format(datetime.now(), acc, ts, cls))
        print(results[-1])
        acc, ts, cls = p.predict_with_knn()
        results.append('[{}] f1: {}; test size: {}; method: {}'.format(datetime.now(), acc, ts, cls))
        print(results[-1])
    
    print('Test completed! Saving to file...')
    with open('network-results.txt', 'a') as file:
        for result in results:
            file.write('{}\n'.format(result))
    print('Results saved!')


if __name__ == "__main__":
    main()
