# Taller: Adquisición, procesamiento y visualización de datos

Nombre: Santiago Ajala Ramos

Objetivo:

● Aprender a manipular datos en varios formatos y con varias herramientas.

● Realizar un análisis de datos exploratorio en un set de datos desconocido.

● Utilizar técnicas de visualización de datos para la exploración.

● Familiarizarse con librerías y herramientas avanzadas en ciencia de datos.

# Parte 1: Adquisición y limpieza de datos

## Realizar la limpieza de los datos explicando la lógica de cada decisión

El primer paso que se hizo fue verificar el tipo de datos de las columnas de nuestro df ya que a veces suelen cambiar. En un inicio las variables _InvoiceNo_, _StockCode_, _Description_, _Country_ y _CustomerID_ tenian el tipo de dato _object_. Sin embargo nos aseguramos que las columnas tengan el tipo de dato _string_ ya que de esta forma se puede manipular mejor los datos faltantes en estas columnas. Debido a que la base de datos contiene transacciones de compras en una tienda online, el segundo paso es eliminar los valore faltantes en la columna _CustomerID_ ya que no tendría sentido que una transacción se haya hecho sin ningún cliente. Por otra parte, las columnas _Quantity_ y _UnitPrice_ representan valores numéricos por lo que filtramos el dataset para que solo nos quedemos con los registros que tienen estas dos columnas mayor a 0 ya que esto hace sentido en la base de datos. Posterior a esto, verificamos si alguna de las transacciones fueron canceladas, buscando las filas que en la columna _InvoiceNo_ empiezen con la letra "C", sin embargo no se encontro ningun caso. Además, en las columnas que son de tipo _string_ nos aseguramos que los registros no tengan espacion en blanco ni al inicio ni al final. Finalmente, imprimimos los valores máximos y mínimos de las variables numericas para comprobar que estamos los valores sean correctos a si como los de la variable _InvoiceDate_ para comprobar que el rango de fechas sea igual al presentado en la documentación. Con todos estos pasos podemos obtener un dataset limpio y listo para guardarlo en una base SQL. 

## Subir los datos limpios a una base de datos SQLite

Para subir el conjunto de datos procesados se utiliza la base de datos MySQL, por lo que sea establece en el código los parámetros para la respectiva conexión. Se realiza la verificación de la tabla creada en la base de datos utilizando MySQL Workbench.

# PARTE 2: EDA

## Análisis y descripción de la información del set de datos

Este dataset contiene datos de transacciones, desde el  01/12/2010 hasta 09/12/2011, realizadas por una empresa de venta al por menor en línea registrada y con sede en el Reino Unido que vende principalmente regalos únicos para toda ocasión y tiene clientes en diferentes países. Luego de realizar la limpieza no aseguramos de que el tipo de cada columna del set de datos tenga el correctp tipo de datos. Adicionalmente se pudo eliminar campos faltante para facilitar un análisis a futuro. Finalmente, se hizo un filtrado utilizando las columnas numéricas para que estas hagan sentido a la idea principal del dataset. Es importante mencionar que en el set de datos había algunas trasacciones que fueron canceladas, sin embargo cuando se aplicó el tratamiento de las columnas numéricas estos fueron eliminados. 


## Describir lo encontrado para cada uno de los campos
Luego de leer los los datos desde la base SQL podemos observar que el set de datos contiene los siguientes campos:

- **InvoiceNo**: Número único de factura
- **StockCode**: Código único del producto
- **Description**: Descripción del producto
- **Quantity**: Cantidad de productos vendidos
- **UnitPrice**: Precio unitario del producto
- **CustomerID**: ID único del cliente
- **InvoiceDate**: Fecha de la transacción
- **Country**: País del cliente

En el caso de la campo _StockCode_, en la documentación especifican que es un campo de 5 dígitos, sin embargo durante la limpieza de datos se logró identificar que algunos registros no cumplian con la condición, sin embargo se reviso dichos registros y se los dejo en el set de datos ya que si aportaban información útil para un futuro análisis.

## ¿Qué meta-data se puede generar?

El principal metadato que se puede crear es el valor total que genera la trasacción, para ello se multiplica el campo _Quantity_ y _UnitPrice_. Por otra parte tambien se puede ver el numero total de transacciones y a esto lo podríamos segmentar ya sea por días, semanas o meses. Tambien se puede ver el día o la hora en la cual se realizarón el mayor número de transacciones. Si nos vamos al tema de clientes podemos observar el número de clientes por país. Además, se podría obtener que clientes son frecuentes o esporádicos. Incluso podemos ver el total de gasto por cliente durante el periodo de análisis. Finalmente, si concideramos desde el punto de productos se puede ver que producto se vendio más o fue el más rentable.

# Parte 3: Visualización

## Top 10 países por número de transacciones

A partir del gráfico, podemos observar que el país con mayor número de transacciones es Reino Unido, con aproximadamente 350,000 transacciones, lo que representa una diferencia significativa respecto al resto de los países. Esta brecha es tan amplia que el segundo país con más transacciones, Alemania, apenas alcanza las 9,000 operaciones. Esta diferencia es esperable, considerando que la tienda está ubicada en el Reino Unido, por lo que la mayoría de las transacciones se concentran en ese país.

## Top 10 productos más vendidos (por cantidad)

La gráfica muestra que los dos productos más vendidos, "PAPER CRAFT, LITTLE BIRDIE" y "MEDIUM CERAMIC TOP STORAGE JAR", superan cada uno las 80,000 unidades, destacándose claramente del resto. A partir del tercer producto, las cantidades vendidas disminuyen de forma progresiva, oscilando entre 30,000 y 55,000 unidades. Esta concentración en los primeros dos ítems sugiere una fuerte preferencia del mercado por ellos, posiblemente por su popularidad, utilidad o estrategia comercial por lo que se podría aumentar el nivel de stock de dichos productos, mientras que el resto del top 10 mantiene una distribución de ventas más equilibrada.

## Transacciones por mes

La gráfica muestra como la cantidad de trasacciones varia en el tiempo. Podemos observer que en los primer meses (12-2010 - 05-2011) la cantidad de transacciones tienen incrementos y decrementos considerables registrandose algunos picos. Por otra parte, a partir del 06-2011 se puede evidenciar como incrementa el número de transacciones hasta llegar a su pico mas alto que fue en noviembre del 2011. En el último mes, se puede ver el decremento drastico en las transacciones, este efecto se genera ya que en este mes solo se registra las transacciones hasta el día 9.

## Heapmap Ventas por semana y hora

El mapa de calor basado revela que las ventas se concentran principalmente entre las 10:00 y las 16:00 horas, siendo el martes a las 12:00 el pico máximo de actividad comercial, seguido por el miércoles a las 12:00 y el martes a las 16:00. También se observa una notable intensidad durante el jueves a mediodía. Los fines de semana, en particular el sábado, presentan una actividad significativamente menor, y el domingo muestra ventas moderadas solo en la mañana y primeras horas de la tarde. Estos patrones sugieren que los días laborales, especialmente a mediodía, son los más activos para la tienda.


    
