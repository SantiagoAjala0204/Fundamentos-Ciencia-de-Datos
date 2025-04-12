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
print("\n Tipo de datos antes:\n", df.dtypes)

#Cambiar a entero la variables CustomerID
df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors='coerce')
df["CustomerID"] = df["CustomerID"].astype('Int64') 

# Cambiar el tipo de dato a las columnas
df["InvoiceNo"]=df["InvoiceNo"].astype('string')
df["StockCode"]=df["StockCode"].astype('string')
df["Description"]=df["Description"].astype('string')
df["Country"]=df["Country"].astype('string')
df["CustomerID"]=df["CustomerID"].astype('string')

print("\n Tipo de datos después de cambiarlos:\n", df.dtypes)

# Revisar valores faltantes en las columnas

def null_values(df):
    for col in df.columns:
        if df[col].isnull().any():
            print(f"La columna {col} tiene valores nulos")
        else:
            print(f"La columna {col} no tiene valores nulos")

print("\n Columnas antes de eliminar valores faltantes\n")
null_values(df)

# Eliminar valores nulos en la columna CustomerID
df = df.dropna(subset=['CustomerID'])
print("\n Columnas después de eliminar valores faltantes\n")
null_values(df)
#Redondear a dos decimales la variables UnitPrice
df['UnitPrice'] = df['UnitPrice'].round(2)

# Filtrar Quantity > 0 o UnitPrice > 0
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Imprimir el tamaño del DataFrame
print(f"\n El tamaño del df es {df.shape}")


# Verificar si hay transacciones canceladas
count = df['InvoiceNo'].str.startswith('C', na=False).sum()
print(f"Hay {count} registros en 'InvoiceNo' que empiezan con 'C'.")

#Pasar a mayusculas la columna Description
df['Description'] = df['Description'].str.upper()

#Eliminar espacios en blanco al inicio y al final de las columnas de tipo string
df = df.apply(lambda x: x.str.strip() if x.dtype == "string[python]" else x)

#Min Quantity
print("Valor min de Cantidad: ",df['Quantity'].min())
# Max Quantity
print("Valor max de Cantidad: ",df['Quantity'].max())
#Ver registros donde quanity es igual a 80995
df[df['Quantity'] == 80995]

# Min UnitPrice
print("Valor min de Valor Cantidad: ",df['UnitPrice'].min())
# Max UnitPrice
print("Valor max de Valor Cantidad: ",df['UnitPrice'].max())

# Min InvoiceDate
print("Fecha min de registros Datset",df['InvoiceDate'].min())
# Max InvoiceDate
print("Fecha max de registros Datset",df['InvoiceDate'].max())

######## StockCode Análisi###
df_prueba=df.copy()
df_prueba['Tamanio']=df_prueba['StockCode'].str.len()
#Filtrar los que tienen tamanio distinto de 6
df_prueba=df_prueba[df_prueba['Tamanio']!=5]
#Selecionar columnas tmanio y descripcion
df_prueba=df_prueba[['Tamanio','Description','InvoiceNo']]
#Agrupar por tamanio y descripcion y cuenta cuantas apariciones hay
df_prueba=df_prueba.groupby(['Tamanio','Description'])['InvoiceNo'].count()
print(df_prueba)
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
# Subir el DataFrame a una tabla nueva
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

#######################  GRAFICAS ############################
import matplotlib.pyplot as plt
import seaborn as sns
# Top 10 países por número de transacciones
ventas_por_pais = df_sql.groupby('Country')['InvoiceNo'].count().sort_values(ascending=False).head(10).reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=ventas_por_pais, x='Country', y='InvoiceNo', hue='Country', palette='Blues_d', legend=False)
plt.title('Cantidad de transacciones por país (Top 10)', fontsize=14)
plt.xlabel('País')
plt.ylabel('Transacciones')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('1_transacciones_por_pais.png')
plt.show()

#2.- Top 10 productos más vendidos (por cantidad)

producto_mas_vendidos = df_sql.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(data=producto_mas_vendidos, x='Quantity', y='Description', hue='Quantity', palette='Reds')
plt.title('Top 10 productos más vendidos', fontsize=14)
plt.xlabel('Cantidad vendida')
plt.ylabel('Producto')
plt.tight_layout()
plt.savefig('2_distribucion_cantidad_productos.png')
plt.show()

#3.- Trasacciones por mes
ventas_por_mes=df_sql.copy()
ventas_por_mes['Mes'] = ventas_por_mes['InvoiceDate'].dt.to_period('M')
ventas_por_mes = ventas_por_mes.groupby('Mes')['Quantity'].sum().reset_index()
ventas_por_mes['Mes'] = ventas_por_mes['Mes'].astype(str)  # Convertir a string para mejor visualización

plt.figure(figsize=(12, 6))
sns.lineplot(data=ventas_por_mes, x='Mes', y='Quantity', marker='o', color='seagreen', linewidth=2)
plt.title('Transacciones por mes', fontsize=14)
plt.xlabel('Mes')
plt.ylabel('Cantidad vendida')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('3_transacciones_por_mes.png')
plt.show()

# 4.- HeatMap
# Copiar el DataFrame 
heap_map_df = df_sql.copy()

# Filtrar ventas del primer mes
heap_map_df = heap_map_df[(heap_map_df['InvoiceDate'] > '2010-12-01') & (heap_map_df['InvoiceDate'] < '2011-01-12')].copy()

# Agregar dias de semana, total (cantidad * precio), hora
heap_map_df.loc[:, 'DiaSemana'] = heap_map_df['InvoiceDate'].dt.day_name()
heap_map_df.loc[:, 'Total'] = heap_map_df['Quantity'] * heap_map_df['UnitPrice']
heap_map_df.loc[:, 'Hora'] = heap_map_df['InvoiceDate'].dt.hour

# Crear tabla dinámica
ventas_heatmap = heap_map_df.pivot_table(
    index='DiaSemana',
    columns='Hora',
    values='Total',
    aggfunc='sum'
)

# Reordenar días de la semana
orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
ventas_heatmap = ventas_heatmap.reindex(orden_dias)

# Graficar el mapa de calor
plt.figure(figsize=(15, 6))
sns.heatmap(ventas_heatmap, cmap='YlGnBu', linewidths=0.5)
plt.title('Valor de las ventas por día de la semana y hora')
plt.xlabel('Hora del día')
plt.ylabel('Día de la semana')
plt.tight_layout()
plt.savefig('4_heatmap_ventas_semana_hora.png')
plt.show()
