import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, roc_auc_score
import matplotlib.pyplot as plt
import joblib  # For saving and loading the model

# Load the dataset from 'data.csv'
df = pd.read_csv('data.csv')

# Create numpy arrays for features and target
X = df.drop('Outcome', axis=1).values
y = df['Outcome'].values

# Split the data into training and test set (40% test, stratified by labels)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42, stratify=y)

# Train k-NN classifier and test for different 'k' values (1 to 8)
neighbors = np.arange(1, 6)
train_accuracy = np.empty(len(neighbors))
test_accuracy = np.empty(len(neighbors))

for i, k in enumerate(neighbors):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    train_accuracy[i] = knn.score(X_train, y_train)
    test_accuracy[i] = knn.score(X_test, y_test)

# Plot the accuracies for different values of k
plt.title('k-NN Varying number of neighbors')
plt.plot(neighbors, test_accuracy, label='Testing Accuracy')
plt.plot(neighbors, train_accuracy, label='Training accuracy')
plt.legend()
plt.xlabel('Number of neighbors')
plt.ylabel('Accuracy')
plt.show()

# Use k=7 (based on accuracy analysis above)
knn_best = KNeighborsClassifier(n_neighbors=10)
knn_best.fit(X_train, y_train)

# Save the trained model
joblib.dump(knn_best, 'knn_model.pkl')

# Evaluate the model on the test set
accuracy = knn_best.score(X_test, y_test)
print(f"Accuracy on the test set: {accuracy}")

# Confusion Matrix
y_pred = knn_best.predict(X_test)
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ROC Curve
y_pred_proba = knn_best.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr, label='k-NN')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('k-NN ROC curve')
plt.show()

# Area under ROC curve
roc_auc = roc_auc_score(y_test, y_pred_proba)
print(f"Area under ROC curve: {roc_auc}")
