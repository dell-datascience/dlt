## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm` ✅


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

```docker
docker run -it python:3.9 bash
```

What is version of the package *wheel* ?

- 0.42.0 ✅
- 1.0.0
- 23.0.1
- 58.1.0


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on 1

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

```sql
SELECT COUNT(*) 
FROM public.green_tripdata_2019_09
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-09-18' AND '2019-09-18'

```

- 15767 ✅
- 15612
- 15859
- 89009

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

```sql
SELECT  DATE(lpep_pickup_datetime) AS pickup_day, SUM(trip_distance)
FROM public.green_tripdata_2019_09
GROUP BY 1
ORDER BY 2 DESC 
```

- 2019-09-18
- 2019-09-16
- 2019-09-26 ✅
- 2019-09-21


## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
 ```sql
 SELECT "Borough" AS Borough, SUM("total_amount") AS total_amount
FROM public.green_tripdata_2019_09 AS green
INNER JOIN taxi_zone_lookup AS lookup
ON green."PULocationID" = lookup."LocationID"
WHERE DATE(lpep_pickup_datetime) = '2019-09-18' AND "Borough" <> 'Unknown'
GROUP BY 1
HAVING SUM("total_amount") > 50000
ORDER BY 2 DESC
 ```
- "Brooklyn" "Manhattan" "Queens" ✅
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"


## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

```sql
SELECT lookup2."Zone", MAX(tip_amount)
FROM public.green_tripdata_2019_09 AS green
INNER JOIN taxi_zone_lookup AS lookup1
ON green."PULocationID" = lookup1."LocationID" 
INNER JOIN taxi_zone_lookup AS lookup2
ON green."DOLocationID" = lookup2."LocationID" 
WHERE EXTRACT('month' FROM DATE(lpep_pickup_datetime)) = 9
	AND lookup1."Zone" = 'Astoria'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1
```
- Central Park
- Jamaica
- JFK Airport ✅
- Long Island City/Queens Plaza



## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

```shell
google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/verdant-catcher-397416/datasets/trips_data_all]
google_storage_bucket.data-lake-bucket: Creation complete after 2s [id=de_data_lake_2024_verdant-catcher-397416]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

Paste the output of this command into the homework submission form.


## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET
