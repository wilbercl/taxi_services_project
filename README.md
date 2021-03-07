# Proyecto Servicios de Taxi 
***
El objetivo de esta prueba es resolver un ejercicio práctico que abarque la extracción de datos, la generación de unas simples web y API de consulta y por último la generación de un entregable en Python.

## Desarrollado  
***
Esta aplicación se implementó utilizando las siguientes tecnologías:

* [Python](https://www.python.org/) - Lenguaje de programación.
* [MySQL](https://www.mysql.com/) - Base de datos.
* [Pandas](https://pandas.pydata.org/) - Manipulación de datos.
* [Django](https://www.djangoproject.com/) - Framework Web usado

## Requerimientos
***
* Python 3.x.x (3.7.9)
* Django 2.2
* Pandas 1.2.2
* MySQL 8.0.2

## Instalación
*** 
- Instalar servidor de mysql, python3, django y pandas (recomiendo crear un entorno virtual que contenga las librerías).
- *pip install -r requirements.txt* (opcional)
- Crear la base de datos con el nombre _taxi_services_
- Ejecutar desde la raiz del proyecto *python manage.py makemigrations* 
- Ejecutar *python manage.py migrate*
- Luego buscar el fichero _tools.py_ y ejecutarlo actualizando la ruta donde se encuentren los ficheros .csv (carga los datos a la base de datos)
- Finalmente ejecutamos *python manage.py runserver* y accedemos a la url desde el navegador (http://127.0.0.1:8000/).

## Preguntas
***
### Part 1. SQL

Procedimiento para cargar los ficheros es ejecutar la siguiente secuencia de código sql por cada fichero con los datos a trabajar. 
``` 
	LOAD DATA INFILE [path_file_csv] 
	INTO TABLE [table_name]
	FIELDS TERMINATED BY ',' 
	ENCLOSED BY '"' 
	LINES TERMINATED BY '\n' 
	IGNORE 1 ROWS 
	[(column_name, …)];
```
#### Definición de la tabla
``` 
	CREATE TABLE IF NOT EXISTS test ( 
		id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
		VendorID SMALLINT UNSIGNED, 
		tpep_pickup_datetime DATETIME NOT NULL, 
		tpep_dropoff_datetime DATETIME NOT NULL, 
		passenger_count INT UNSIGNED NOT NULL, 
		trip_distance DECIMAL(10 , 2 ) NOT NULL, 
		RatecodeID SMALLINT UNSIGNED NOT NULL, 
		store_and_fwd_flag VARCHAR(50) NOT NULL, 
		PULocationID INT NOT NULL, 
		DOLocationID INT NOT NULL, 
		payment_type SMALLINT UNSIGNED NOT NULL, 
		fare_amount DECIMAL(10 , 2 ) NOT NULL, 
		extra DECIMAL(10 , 2 ) NOT NULL, 
		mta_tax DECIMAL(10 , 2 ) NOT NULL, 
		tip_amount DECIMAL(10 , 2 ) NOT NULL, 
		tolls_amount DECIMAL(10 , 2 ) NOT NULL, 
		improvement_surcharge DECIMAL(10 , 2 ) NOT NULL, 
		total_amount DECIMAL(10 , 2 ) NOT NULL, 
		congestion_surcharge DECIMAL(10 , 2 ) NOT NULL );
```

Establecer una política de la calidad de datos es una necesidad que se prolonga en el tiempo. La gestión manual y/o automatizada de la calidad de los datos ha de velar por la calidad de los mismos, y su tratamiento dependerá de la necesidades del análisis. En los datos propuestos se encontraron varias incongruencias e errores, los cuales fueron eliminados, como por ejemplo:
* En los registros habían fechas que no correspondían con los meses de _enero_, _febrero_ y _marzo_ de _2020_.
* Existían datos en la columna _tpep_dropoff_datetime_ que representa la fecha y hora en que se desactivó el medidor, inferior a la columna _tpep_pickup_datetime_ que representa la fecha y hora en que se activó el medidor.
* En la columna _trip_distance_ que representa la distancia del viaje transcurrida en millas informada por el taxímetro, estaban con valores menores o igual (<=) a 0.
* En la columna _fare_amount_ que representa la tarifa de tiempo y distancia calculada por el medidor, estaban con valores menores o igual (<=) a 0.
* En la columna _tolls_amount_ que representa el importe total de todos los peajes pagados en el viaje, estaban con valores menor (<) a 0.
* En la columna _extra_ que representa extras y recargos varios, estaban con valores menor (<) a 0.
* En la columna _mta_tax_ que representa el impuesto MTA de $ 0.50 que se activa automáticamente según la tarifa medida en uso, estaban con valores menor (<) a 0. 

#### Cantidad de registros en la tabla: 15500876

```
SELECT COUNT(*) FROM [table_name]
```

#### * Trayecto en distancia
```
 SELECT * 
 FROM ( 
 		SELECT DATE_FORMAT(tpep_pickup_datetime, '%Y-%m') as mes, 
 			   MAX(trip_distance) as mayor, 
 			   MIN(trip_distance) as menor, 
 			   AVG(trip_distance) as media 
 		FROM test 
 		GROUP BY mes 
 		) test 
 ORDER BY mes;
 ```
|mes| mayor| menor| medio|
|---|------|------|------|
| 2020-01| 210240.07| 0.01| 2.97|
| 2020-02| 57051.09| 0.01| 2.89|
| 2020-03 |269803.73| 0.01 |3.15|

#### * Trayecto en tiempo (diferencia en minute entre la fecha de recogida (_tpep_pickup_datetime_) y la fecha de llegada (_tpep_dropoff_datetime_))
```
SELECT * 
FROM ( 
		SELECT DATE_FORMAT(tpep_pickup_datetime, '%Y-%m') as mes, 
		       MAX(TIMESTAMPDIFF(minute,tpep_pickup_datetime, tpep_dropoff_datetime)) as mayor, 
		       MIN(TIMESTAMPDIFF(minute,tpep_pickup_datetime, tpep_dropoff_datetime)) as menor, 
		       AVG(TIMESTAMPDIFF(minute,tpep_pickup_datetime, tpep_dropoff_datetime)) as media 
		FROM test 
		GROUP BY mes
	 ) test 
ORDER BY mes; 
```
|mes| mayor| menor| medio|
|---|------|------|------|
|2020-01| 8525| 0| 15.52|
|2020-02| 2632| 0| 15.72|
|2020-03| 1814| 0 |15.18|

#### * Variacion porcentual respecto al mes anterior
```
SELECT mes, 
	   servicios, 
	   CONCAT(ROUND(100 * (servicios / LAG(servicios) OVER (ORDER BY mes) - 1)), '%') variacion_mes_anterior 
FROM ( 
		SELECT DATE_FORMAT(tpep_pickup_datetime, '%Y-%m') mes, 
		       COUNT(*) servicios 
		FROM test 
		GROUP BY mes
	  ) subquery 
ORDER BY mes;
```

|mes |servicios| variacion_mes_anterior|
|----|---------|-----------------------|
| 2020-01| 6316295| NULL|
| 2020-02| 6219699| -2%|
| 2020-03| 2964882| -52%|

### Part 2. Django, Web, API
Ejemplo de la url del sitio web
http://127.0.0.1:8000/services/
#### Parte 2.2. API Endpoint para consultar los servicios
http://127.0.0.1:8000/services/longest_trips?vendor_id=1&limit=3

Ejemplo del .json resultante
```
{
    "servicios": [
        {
            "vendor_id": 1,
            "tpep_pickup_datetime": "2020-02-01T00:26:31",
            "tpep_dropoff_datetime": "2020-02-01T00:52:26",
            "trip_distance": "7.50"
        },
        {
            "vendor_id": 1,
            "tpep_pickup_datetime": "2020-03-01T00:14:43",
            "tpep_dropoff_datetime": "2020-03-01T00:37:00",
            "trip_distance": "7.20"
        },
        {
            "vendor_id": 1,
            "tpep_pickup_datetime": "2020-03-01T00:15:43",
            "tpep_dropoff_datetime": "2020-03-01T00:46:57",
            "trip_distance": "6.20"
        }
    ]
}
```

### Part 3. Generar un informe usando python
Ejecutar el script _excel_file_generator.py_

## Versionado
***
Git

## Autor
***
Wilber Concepción Lugo