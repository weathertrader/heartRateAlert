

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


if __name__ == '__main__':
        
    batch_duration = 1
    spark_context = SparkContext('local[2]', appName='PythonStreamingCountByValue')
    stream_context = StreamingContext(spark_context, batch_duration)    

    
    lines = stream_context.socketTextStream('localhost', 9999)


    words = lines.flatMap(lambda line: line.split(" "))
    
    # Count each word in each batch
    pairs = words.map(lambda word: (word, 1))
    wordCounts = pairs.reduceByKey(lambda x, y: x + y)
    
    # Print the first ten elements of each RDD generated in this DStream to the console
    wordCounts.pprint()

    #data = ds.map(lambda line: int(line.split(',')))
    #[dum1, dum2, dum3, dum4] = ds.map(lambda line: int(line.split(',')))
    
    #data_count = data.countByValue()
    #data_count.pprint()
    #data.pprint()
    #print('values are %s %s %s %'%(dum1, dum2, dum3, dum4))
    #print('data is   %s '%(data))
    #print(type(data))
    stream_context.start()
    
    stream_context.awaitTermination()

# spark = SparkSession \
#     .builder \
#     .appName("StructuredNetworkWordCount") \
#     .getOrCreate()
        
# # Create DataFrame representing the stream of input lines from connection to localhost:9999
# lines = spark \
#     .readStream \
#     .format("socket") \
#     .option("host", "localhost") \
#     .option("port", 9999) \
#     .load()

# # Split the lines into words
# words = lines.select(
#    explode(
#        split(lines.value, " ")
#    ).alias("word")
# )

# # Generate running word count
# wordCounts = words.groupBy("word").count()

# # Start running the query that prints the running counts to the console
# query = wordCounts \
#     .writeStream \
#     .outputMode("complete") \
#     .format("console") \
#     .start()

# query.awaitTermination()

