import boto3
import psycopg2
def lambda_handler(event,context):
    aws_access_key_id = 'xxxxxxxxxxxxxxxxxxxx'
    aws_secret_access_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    s3resource=boto3.resource('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name='us-east-2(any_region)')
    bucket=s3resource.Bucket("Bucket_Name")
    print(event)


    if event['Records'][0]['Sns']['Message']=="SUCCESSFUL":

        #bucket1=event['Records'][0]['s3']['bucket']['name']
        #key=event['Records'][0]['s3']['object']['key']
        #key_format=key.split('.')[0]
        schema ='public'
        dbname = 'patient'
        port = 5439
        user = 'xxxxxxxxx'
        password = 'xxxxxxxx'
        file_path_origin = 's3://xxxxxxx/'
        host_url = 'xxxxxxxxxx.redshift.amazonaws.com'
        conn_string = "dbname='patient' port='5439' user='xxxxxx' password='xxxxxxxxx' host='xxxxxxxxxx.redshift.amazonaws.com'"
        con = psycopg2.connect(conn_string)
        client=boto3.client('s3',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name='us-east-2')

        cur = con.cursor()

        tables1=['st_df_ANATOMY','st_df_MEDICAL_CONDITION','st_df_MEDICATION','st_df_PROTECTED_HEALTH_INFORMATION','st_df_TEST_TREATMENT_PROCEDURE','st_BRANDNAME','st_GENERICNAME','PATIENT_DATA','st_PROCEDURES','st_TESTS','st_TREATMENTS']
        tables2=['display_ANATOMY','display_BRANDNAME','display_GENERICNAME','display_TESTS','display_PROCEDURES']
        tables3=['st_NEGATION','st_SYMPTOM','st_DIAGNOSIS','st_SIGN']


        def original_column_count(table_name):
            file_path = file_path_origin+table_name+'.csv'
            drop_table_query='drop table IF EXISTS {};'.format(table_name)
            create_table_query='create table {} (Id varchar(2),category varchar(100),score varchar(100),type varchar(100),traits_name varchar(100),traits_score varchar(100),text varchar(100),attributes_type varchar(100),attributes_text varchar(100),attributes_score varchar(100),unmappedattributes varchar(100));'.format(table_name)
            sql="copy {}.{} from '{}'\
                    credentials \
                    'aws_access_key_id={};aws_secret_access_key={}' \
                    CSV IGNOREHEADER 1;"\
                    .format(schema, table_name, file_path, aws_access_key_id, aws_secret_access_key)
            cur.execute(drop_table_query)
            cur.execute(create_table_query)
            cur.execute(sql)

        
            
        def display_column_count(table_name):
            file_path = file_path_origin+table_name+'.csv'
            drop_table_query='drop table IF EXISTS {};'.format(table_name)
            create_table_query='create table {} (score varchar(20), text varchar(20));'.format(table_name)
            sql="copy {}.{} from '{}'\
                    credentials \
                    'aws_access_key_id={};aws_secret_access_key={}' \
                    CSV IGNOREHEADER 1;"\
                    .format(schema, table_name, file_path, aws_access_key_id, aws_secret_access_key)
            cur.execute(drop_table_query)
            cur.execute(create_table_query)
            cur.execute(sql)


        
        def traits_column(table_name):
            file_path = file_path_origin+table_name+'.csv'
            drop_table_query='drop table IF EXISTS {};'.format(table_name)
            create_table_query='create table {} (text varchar(20),score varchar(20));'.format(table_name)
            sql="copy {}.{} from '{}'\
                    credentials \
                    'aws_access_key_id={};aws_secret_access_key={}' \
                    CSV IGNOREHEADER 1;"\
                    .format(schema, table_name, file_path, aws_access_key_id, aws_secret_access_key)
            cur.execute(drop_table_query)
            cur.execute(create_table_query)
            cur.execute(sql)


        def medication_table():    
            table_name='st_MEDICATION'
            file_path = file_path_origin+table_name+'.csv'
            drop_table_query='drop table IF EXISTS {};'.format(table_name)
            create_table_query='create table {} (MEDICATION VARCHAR(50),STRENGTH VARCHAR(50),FORM VARCHAR(50),DOSAGE VARCHAR(50),FREQUENCY VARCHAR(50),ROUTE_OR_MODE VARCHAR(50),DURATION VARCHAR(50));'.format(table_name)
            sql="copy {}.{} from '{}'\
                    credentials \
                    'aws_access_key_id={};aws_secret_access_key={}' \
                    CSV IGNOREHEADER 1;"\
                    .format(schema, table_name, file_path, aws_access_key_id, aws_secret_access_key)
            cur.execute(drop_table_query)
            cur.execute(create_table_query)
            cur.execute(sql)


        def medication_with_scores_table():
            table_name='st_MEDICATION_WITH_SCORES'
            file_path = file_path_origin+table_name+'.csv'
            drop_table_query='drop table IF EXISTS {};'.format(table_name)
            create_table_query='create table {} (MEDICATION VARCHAR(100),STRENGTH VARCHAR(100),STRENGTH_SCORE VARCHAR(100),FORM VARCHAR(100),FORM_SCORE VARCHAR(100),DOSAGE VARCHAR(100),DOSAGE_SCORE VARCHAR(100),FREQUENCY VARCHAR(100),FREQUENCY_SCORE VARCHAR(100),ROUTE_OR_MODE VARCHAR(100),ROUTE_OR_MODE_SCORE VARCHAR(100),DURATION VARCHAR(100),DURATION_SCORE VARCHAR(100));'.format(table_name)
            sql="copy {}.{} from '{}'\
                    credentials \
                    'aws_access_key_id={};aws_secret_access_key={}' \
                    CSV IGNOREHEADER 1;"\
                    .format(schema, table_name, file_path, aws_access_key_id, aws_secret_access_key)
            cur.execute(drop_table_query)
            cur.execute(create_table_query)
            cur.execute(sql)
        
        for each_file in bucket.objects.all():
            key=(each_file.key).split(".")[0]
            if key in tables1:
                original_column_count(key)
            elif key in tables2:
                display_column_count(key)
            elif key in tables3:
                traits_column(key)
            elif each_file.key=='st_MEDICATION.csv':
                medication_table()
            elif each_file.key=='st_MEDICATION_WITH_SCORES.csv':
                medication_with_scores_table()


        con.commit()
        con.close()
        cur.close()

        print("uploded to redshift")