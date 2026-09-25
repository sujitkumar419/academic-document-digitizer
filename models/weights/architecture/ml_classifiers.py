from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import joblib

def get_ml_classifiers():
    models_dict = {
        'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'naive_bayes': GaussianNB(),
        'svm': SVC(probability=True, random_state=42)
    }
    return models_dict

def train_and_save_classifier(model_name, clf, X_train, y_train, save_path):
    clf.fit(X_train, y_train.ravel())
    joblib.dump(clf, save_path)
    return clf

def load_classifier(load_path):
    return joblib.load(load_path)