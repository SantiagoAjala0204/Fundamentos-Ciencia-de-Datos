import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

#PARTE 1
#1.- Leer el archivo Excel 
df = pd.read_excel('C:/Users/USUARIO/Desktop/Maestría_Ciencia_Datos/2.- Fundamentos Ciencia de Datos/Online Retail.xlsx')
print(df.head())

#########################################################################

# 2.- Limpieza de los datos

# Imprimir el tipo de datos de las columnas
print("\n Tipo de datos antes:", df.dtypes)

# Cambiar el tipo de dato a las columnas
df["InvoiceNo"]=df["InvoiceNo"].astype('string')
df["StockCode"]=df["StockCode"].astype('string')
df["Description"]=df["Description"].astype('string')
df["Country"]=df["Country"].astype('string')
df["CustomerID"]=df["CustomerID"].astype('string')

print("\n Tipo de datos después de cambiarlos:", df.dtypes)

# Revisar valores faltantes en las columnas

def null_values(df):
    for col in df.columns:
        if df[col].isnull().any():
            print(f"La columna {col} tiene valores nulos")
        else:
            print(f"La columna {col} no tiene valores nulos")

print("\n Columnas antes de eliminar valores faltantes")
null_values(df)

# Eliminar valores nulos en la columna CustomerID
df = df.dropna(subset=['CustomerID'])
print("\n Columnas después de eliminar valores faltantes")
null_values(df)

# Filtrar Quantity > 0 o UnitPrice > 0
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Imprimir el tamaño del DataFrame
print(f"\n El tamaño del df es {df.shape}")

# Convertir la columna InvoiceDate a tipo datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Verificar si hay transacciones canceladas
count = df['InvoiceNo'].str.startswith('C', na=False).sum()
print(f"Hay {count} registros en 'InvoiceNo' que empiezan con 'C'.")

###########################################################
# 3.- Subir los datos limpios a una base de datos SQLite
## Conectar a la base de datos MySQL
# Parámetros de conexión
usuario = 'root'
contrasena = ''  
host = 'localhost'
puerto = '3306'
nombre_bd = 'online_store'

#Guardar el df en MySQL
# Crear la conexión usando SQLAlchemy y pymysql
conexion_load = create_engine(f"mysql+pymysql://{usuario}:{contrasena}@{host}:{puerto}/{nombre_bd}")
# Subir el DataFrame a una tabla nueva (ej. 'ventas'), reemplazándola si ya existe
df.to_sql(name='online_retails', con=conexion_load, if_exists='replace', index=False)

print("✅ ¡Datos subidos exitosamente a la base de datos!")

#PARTE2 
#Leer la tabla desde MySQL y guardarla en un DataFrame
# Crear la conexión usando mysql-connector
conexion = mysql.connector.connect(
    host=host,
    user=usuario,
    password=contrasena,
    database=nombre_bd
)

# Verificar si la conexión fue exitosa
if conexion.is_connected():
    print("Conexión exitosa a la base de datos")
else:
    print("Error al conectar a la base de datos")

# Leer los datos desde MySQL
query = "SELECT * FROM online_retails;"
df_sql = pd.read_sql(query, con=conexion)
# Cerrar la conexión
conexion.close()
# Mostrar los primeros registros
print(df_sql.head())
