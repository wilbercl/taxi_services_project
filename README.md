#Taxi Services Project 
***
The objective of the test is to see how you develop in a practical exercise that covers data extraction, the generation of a simple web and query API and finally the generation of a deliverable in Python.

##Requirements 
***
* Python 3.x.x (3.6.10) 

* Running the application (Local)

* DataBase: MySQL

*Pandas 2
*Django 2.2

##Installation
*** 

##Questions
***
Part 1. SQL

Procedimiento para cargar los ficheros es ejecutar la siguiente secuencia de código sql por cada fichero con los datos a trabajar. 
``` 
	LOAD DATA INFILE [path_file_csv] 
	INTO TABLE [table_name]
	FIELDS TERMINATED BY ',' 
	ENCLOSED BY '"' 
	LINES TERMINATED BY '\n' 
	IGNORE 1 ROWS • [(column_name, …)];
```
###Table definition
***
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

Cantidad de registros de la tabla (excluidos los registros con fechas diferentes a enero, febrero y marzo de 2020 y, los registros con trip_distance <=0 (162070) y los registros en donde la columna trep_dropoff_datetime es inferior a la de trep_pickup_datetime (4), fare_amount <=0 (48417), Tolls_amount<0 (1), extra <0 (4), MTa_tax <0 (7), ) son 15500876.
```
SELECT COUNT(*) FROM [table_name]
```

###Trayecto en distancia
***
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

###Trayecto en tiempo (diferencia en minute entre la fecha de recogida y la fecha de llegada) 
***
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

###Variacion porcentual respecto al mes anterior
***
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

##Author
***
Wilber Concepción Lugo