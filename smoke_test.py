"""Generated-data smoke test only. Outputs are NOT research evidence."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=120, n_features=8, n_informative=5,
                           n_redundant=1, n_classes=3, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
model = RandomForestClassifier(n_estimators=20, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("SMOKE TEST ONLY — generated toy data; do not cite as project findings.")
print(f"Generated rows: {len(X)}; training rows: {len(X_train)}; test rows: {len(X_test)}")
print(f"Pipeline ran successfully; toy-data accuracy: {accuracy_score(y_test, pred):.3f}")
