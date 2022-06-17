from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType
from pyspark.sql.types import StringType
from pyspark.sql.functions import lit
import json
from pyspark.sql import SparkSession, Row


builder = SparkSession.builder \
        .appName("Spark NLP Licensed") \
        .master("spark://spark-master:7077") \
        .config("spark.driver.memory", "20G") \
        .config("spark.executor.memory", "2G") \
        .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:3.4.2") \
        .config("spark.sql.parquet.columnarReaderBatchSize", 100) \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
spark = builder.getOrCreate()
spark.sparkContext.setLogLevel("OFF")


dataDF = spark.read.json ('/prueba_json_en')
number = dataDF.count()
print (number)


from pyspark.sql.functions import udf

import datetime

import requests
import json

transString = 'http://intelcomp.bsc.es/translate'
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

def translateBSC (strdata):
    dataTrans = {'text':strdata}
    result = requests.post (transString, headers=headers, data=json.dumps(dataTrans))
    return result.text


translate_udf = udf (lambda x: translateBSC(x), StringType())


from datetime import datetime


start_time = datetime.now()

dataDF = dataDF.withColumn ('paperAbstractTranslate', translate_udf (dataDF.paperAbstract))

savePath = '/export/ml4ds/temporal/prueba_' + str(number)

dataDF.write.mode('overwrite').parquet (savePath)

end_time = datetime.now()
print (number)
print('Duration: {}'.format(end_time - start_time))


