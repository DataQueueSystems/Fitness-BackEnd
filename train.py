import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

data = pd.read_csv("DietChartPlan.csv")

label_encoder_DietName = LabelEncoder()
data['DietName_encoded'] = label_encoder_DietName.fit_transform(data['DietName'])

label_encoder_DietType = LabelEncoder()
data['DietType_encoded'] = label_encoder_DietType.fit_transform(data['DietType'])

X = data[['DietName_encoded', 'DietType_encoded', 'Protein', 'Calories']].values
y = data['FoodName'].values

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=0)


classifier = RandomForestClassifier(n_estimators=10, random_state=0)
classifier.fit(X_train, y_train)


with open("ModelFile.pkl", "wb") as model_file:
    pickle.dump((classifier, label_encoder_DietName, label_encoder_DietType), model_file)
