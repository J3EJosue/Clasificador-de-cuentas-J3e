import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
import re
import os
import joblib

# Rutas a los archivos
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tu_archivo.csv')
model_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'modelo_guardado.joblib')

# Variables globales
df = None
vectorizer = None
naturaleza_model = None
libros_model = None
description_model = None
mlb = None

def normalize_text(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', str(text).lower())

def load_model():
    global df, vectorizer, naturaleza_model, libros_model, description_model, mlb
    
    if df is None:
        df = pd.read_csv(csv_path)
        print("Columnas en el DataFrame:", df.columns)  # Añade esta línea para depuración
        
        # Asegúrate de que las columnas necesarias existan
        required_columns = ['Nombre de la cuenta', 'Naturaleza ampliada', 'Libros contables relevantes', 'Descripción']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"La columna '{col}' no está presente en el CSV.")
        
        df['Nombre normalizado'] = df['Nombre de la cuenta'].apply(normalize_text)
        
        if os.path.exists(model_path):
            model_data = joblib.load(model_path)
            vectorizer = model_data['vectorizer']
            naturaleza_model = model_data['naturaleza_model']
            libros_model = model_data['libros_model']
            description_model = model_data['description_model']
            mlb = model_data['mlb']
        else:
            X = df['Nombre normalizado']
            y_naturaleza = df['Naturaleza ampliada']
            
            df['Libros contables'] = df['Libros contables relevantes'].apply(lambda x: [libro.strip() for libro in str(x).split(',')])
            mlb = MultiLabelBinarizer()
            y_libros = mlb.fit_transform(df['Libros contables'])
            
            vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=5000)
            X_vectorized = vectorizer.fit_transform(X)
            
            naturaleza_model = MultinomialNB()
            naturaleza_model.fit(X_vectorized, y_naturaleza)
            
            libros_model = MultiOutputClassifier(MultinomialNB())
            libros_model.fit(X_vectorized, y_libros)
            
            description_model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500)
            description_model.fit(X_vectorized, df['Descripción'])
            
            model_data = {
                'vectorizer': vectorizer,
                'naturaleza_model': naturaleza_model,
                'libros_model': libros_model,
                'description_model': description_model,
                'mlb': mlb
            }
            joblib.dump(model_data, model_path)

def get_similar_accounts(query_vec, top_n=5):
    similarities = cosine_similarity(query_vec, vectorizer.transform(df['Nombre normalizado'])).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]
    return df.iloc[top_indices], similarities[top_indices]

def sugerir_libros_adicionales(naturaleza, libros_actuales):
    libros_sugeridos = set(libros_actuales)
    if "Activo" in naturaleza or "Pasivo" in naturaleza:
        libros_sugeridos.add("Balance General")
        libros_sugeridos.add("Balance de Saldos")
    if "Ingreso" in naturaleza or "Gasto" in naturaleza:
        libros_sugeridos.add("Estado de Resultados")
    if "Costo" in naturaleza:
        libros_sugeridos.add("Estado de Costo de Producción")
        libros_sugeridos.add("Estado de Costo de Ventas")
    return list(libros_sugeridos)

def generar_ejemplo_transaccion(naturaleza, nombre_cuenta):
    if "Activo" in naturaleza:
        return f"Ejemplo de transacción: Aumento en {nombre_cuenta} / Abono a Bancos"
    elif "Pasivo" in naturaleza:
        return f"Ejemplo de transacción: Aumento en Bancos / Abono a {nombre_cuenta}"
    elif "Ingreso" in naturaleza:
        return f"Ejemplo de transacción: Aumento en Bancos / Abono a {nombre_cuenta}"
    elif "Gasto" in naturaleza:
        return f"Ejemplo de transacción: Cargo a {nombre_cuenta} / Abono a Bancos"
    else:
        return "No se pudo generar un ejemplo de transacción para esta cuenta."

def generar_descripcion(cuenta_vec, naturaleza, libros, nombre_cuenta):
    base_description = description_model.predict(cuenta_vec)[0]
    libros_str = ", ".join(libros)
    expanded_description = f"{base_description} La cuenta '{nombre_cuenta}' es una cuenta de {naturaleza.lower()} que se utiliza principalmente en {libros_str}. "
    
    if "activo" in naturaleza.lower():
        expanded_description += "Representa recursos económicos propiedad de la empresa. "
    elif "pasivo" in naturaleza.lower():
        expanded_description += "Representa obligaciones o deudas de la empresa. "
    elif "capital" in naturaleza.lower():
        expanded_description += "Representa la inversión de los propietarios en la empresa. "
    elif "ingreso" in naturaleza.lower():
        expanded_description += "Representa aumentos en los beneficios económicos de la empresa. "
    elif "gasto" in naturaleza.lower() or "perdida" in naturaleza.lower():
        expanded_description += "Representa disminuciones en los beneficios económicos de la empresa. "
    
    for libro in libros:
        if "Balance General" in libro:
            expanded_description += "Se presenta en el Balance General, reflejando la situación financiera de la empresa. "
        elif "Estado de Resultados" in libro:
            expanded_description += "Se presenta en el Estado de Resultados, mostrando el desempeño financiero de la empresa. "
        elif "Costo de Producción" in libro:
            expanded_description += "Se utiliza en el Estado de Costo de Producción para determinar el costo de los productos fabricados. "
        elif "Costo de Ventas" in libro:
            expanded_description += "Se emplea en el Estado de Costo de Ventas para calcular el costo de los productos vendidos. "
    
    expanded_description += generar_ejemplo_transaccion(naturaleza, nombre_cuenta)
    
    return expanded_description

def clasificar_cuenta(nombre_cuenta):
    load_model()
    nombre_normalizado = normalize_text(nombre_cuenta)
    cuenta_vec = vectorizer.transform([nombre_normalizado])
    
    similar_accounts, similarities = get_similar_accounts(cuenta_vec)
    
    if similarities[0] > 0.9:
        info = similar_accounts.iloc[0]
        naturaleza = info['Naturaleza ampliada']
        libros = info['Libros contables relevantes'].split(',') if 'Libros contables relevantes' in info else []
        fuente = "CSV (cuenta encontrada)"
        confianza = f"Alta (similitud: {similarities[0]:.2f})"
    else:
        naturaleza = naturaleza_model.predict(cuenta_vec)[0]
        libros_pred = libros_model.predict(cuenta_vec)[0]
        libros = mlb.classes_[libros_pred.astype(bool)].tolist()
        fuente = "Predicción del modelo"
        confianza = f"Media (mejor similitud: {similarities[0]:.2f})"
    
    libros_sugeridos = sugerir_libros_adicionales(naturaleza, libros)
    descripcion = generar_descripcion(cuenta_vec, naturaleza, libros_sugeridos, nombre_cuenta)
    
    return {
        "nombre_cuenta": nombre_cuenta,
        "naturaleza": naturaleza,
        "libros": libros_sugeridos,
        "descripcion": descripcion,
        "fuente": fuente,
        "similar_accounts": similar_accounts.to_dict('records'),
        "confianza": confianza
    }

# Cargar el modelo al iniciar
load_model()
print("Modelo cargado y listo para clasificar")