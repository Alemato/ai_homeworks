import datetime

import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor


def train_regressor():
    df = pd.read_csv('../csv/eval_dataset.csv')
    # Separare le features e il target
    X = df.drop('HL', axis=1)  # Features: h1 a h20
    y = df['HL']  # Target: HL

    # Divisione del dataset in set di addestramento e di validazione
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Creazione del modello MLPRegressor
    mlp_regressor = MLPRegressor(hidden_layer_sizes=(100, 50),
                                 activation='relu',
                                 solver='adam',
                                 alpha=0.0001,
                                 learning_rate_init=0.001,
                                 max_iter=500,
                                 early_stopping=True,
                                 validation_fraction=0.1,
                                 n_iter_no_change=10,
                                 random_state=42,
                                 verbose=True)

    # Addestramento del modello
    mlp_regressor.fit(X_train, y_train)

    # Valutazione del modello sul set di validazione
    y_val_pred = mlp_regressor.predict(X_val)
    mse = mean_squared_error(y_val, y_val_pred)
    r2 = r2_score(y_val, y_val_pred)

    print(f"Errore Quadratico Medio sul set di validazione: {mse}")
    print(f"Coefficiente di determinazione (R²) sul set di validazione: {r2}")

    # Salvare il modello addestrato
    joblib.dump(mlp_regressor, 'mlp_regressor_model_c_64.joblib')

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print(f"Addestramento iniziato a: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    train_regressor()

    end_time = datetime.datetime.now()
    print(f"Addestramento terminato a: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Durata totale: {end_time - start_time}")