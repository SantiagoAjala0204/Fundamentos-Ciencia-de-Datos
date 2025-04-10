# Taller: Adquisición, procesamiento y visualización de datos

Nombre: Santiago Ajala Ramos

Objetivo:

● Aprender a manipular datos en varios formatos y con varias herramientas.

● Realizar un análisis de datos exploratorio en un set de datos desconocido.

● Utilizar técnicas de visualización de datos para la exploración.

● Familiarizarse con librerías y herramientas avanzadas en ciencia de datos.

# Parte 1: Adquisición y limpieza de datos

## Realizar la limpieza de los datos explicando la lógica de cada decisión

El primer paso que se hizo fue verificar el tipo de datos de las columnas de nuestro df ya que a veces suelen cambiar. En un inicio las variables _InvoiceNo_, _StockCode_, _Description_, _Country_ y _CustomerID_ tenian el tipo de dato _object_. Sin embargo nos aseguramos que las columnas tengan el tipo de dato _string_ ya que de esta forma se puede manipular mejor los datos faltantes en estas columnas. Debido a que la base de datos contiene transacciones de compras en una tienda online, el segundo paso es eliminar los valore faltantes en la columna _CustomerID_ ya que no tendría sentido que una transacción se haya hecho sin ningún cliente. Por otra parte, las columnas _Quantity_ y _UnitPrice_ representan valores numéricos por lo que filtramos el dataset para que solo nos quedemos con los registros que tienen estas dos columnas mayor a 0 ya que esto hace sentido en la base de datos. Posterior a esto, transformamos la variable _InvoiceDate_ a tipo _datetime_ para solo tener la fecha en donde se realizo la transacción. Finalmente, verificamos si alguna de las transacciones fueron canceladas, buscando las filas que en la columna _InvoiceNo_ empiezen con la letra "C", sin embargo no se encontro ningun caso. Con todos estos pasos podemos obtener un dataset limpio y listo para guardarlo en una base SQL. 
