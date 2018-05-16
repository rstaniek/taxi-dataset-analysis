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


class Program:
    url = "C:/Users/rajmu/Desktop/project-4/crimes_ML_ready.csv"
    validation_size = -1
    seed = -1

    def __init__(self):
        self.dataset = pandas.read_csv(Program.url, sep=';', low_memory=False)
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
        Program.validation_size = 0.9
        Program.seed = 7
        return model_selection.train_test_split(X, Y, test_size=Program.validation_size, random_state=Program.seed)

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
        knn = KNeighborsClassifier()
        x_train, x_validation, y_train, y_validation = Program.__split_validation_dataset(self)
        knn.fit(x_train, y_train)
        predictions = knn.predict(x_validation)
        print(accuracy_score(y_validation, predictions))
        print(confusion_matrix(y_validation, predictions))
        print(classification_report(y_validation, predictions))


def main():
    p = Program()
    print(p.dataset.describe())
    #p.test_models()
    p.predict_with_knn()
    p.show_histogram()


if __name__ == "__main__":
    main()
