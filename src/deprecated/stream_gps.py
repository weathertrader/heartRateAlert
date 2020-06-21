


if __name__ == "__main__":
    #if len(sys.argv) != 3:
    #    print("Usage: structured_network_wordcount.py <hostname> <port>", file=sys.stderr)
    #    sys.exit(-1)
    #host = sys.argv[1]
    #port = int(sys.argv[2])

    spark = SparkSession\
        .builder\
        .appName("stream_gps")\
        .getOrCreate()

    # Task configuration.
    topic = "heartbeat"
    brokerAddresses = "localhost:9092"
    batchTime = 1
    
    # Creating stream.
    spark = SparkSession.builder.appName("PythonHeartbeatStreaming").getOrCreate()
    sc = spark.sparkContext
    ssc = StreamingContext(sc, batchTime)    
    



    # Create DataFrame representing the stream of input lines from connection to host:port
    #lines = spark\
    #    .readStream\
    #    .format('socket')\
    #    .option('host', host)\
    #    .option('port', port)\
    #    .load()

    #df = spark \
    #  .readStream \
    #  .format("kafka") \
    #  .option("kafka.bootstrap.servers", "xx.xx.xx.xx:9092") \
    #  .option("subscribe", "test") \
    #  .load()    

    # Similar to definition of staticInputDF above, just using `readStream` instead of `read`
    #df = spark
    #    .readStream                       
    #    .schema(jsonSchema)               # Set the schema of the JSON data
    #    .option("maxFilesPerTrigger", 1)  # Treat a sequence of files as a stream by picking one file at a time
    #    .json(inputPath)
    #)

    #file_name_input = 'data_temp.csv'
    #print(os.path.isfile(file_name_input))

    # create Spark context with Spark configuration
    #conf = SparkConf().setAppName("read text file in pyspark")
    #sc = SparkContext(conf=conf)



    #print('print lines begin ')
    
    # Read file into RDD
    #lines = sc.textFile(file_name_input)
    # Call collect() to get all data
    #llist = lines.collect()
    
    # print line one by line
    #for line in llist:
    #    print(line)

    #print('read static_df begin ')
    #static_df = spark.read.format('csv').options(header='true', inferSchema='true').load(file_name_input)
    #static_df = sc.read.format('csv').options(header='true', inferSchema='true').load(file_name_input)
    #print('print static_df begin ')
    #print(static_df)    
    #print('print static_df end ')

    print('mark01 ')
    # Create DataFrame representing the stream of input lines from connection to localhost:9999
    
    lines = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999)

    lines = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999)

    #lines = spark \
    #    .readStream \
    #    .format("socket") \
    #    .option("host", "localhost") \
    #   .option("port", 9999) \
    #   .load()


    print(lines)
    
    # Starting the task run.
    ssc.start()
    ssc.awaitTermination()



    print('mark02 ')
    for line in lines:
        print(line)

    print('mark03 ')

    # Read all the csv files written atomically in a directory
    userSchema = StructType().add("dum", "string").add("dt", "string").add("user", "integer").add("lon", "string").add("lat", "integer")

    data_df = spark \
      .readStream \
      .format("csv") \
      .option("sep", ",") \
      .option("header", "true") \
      .schema(userSchema) \
      .load(file_name_input)

    print('write data begin ')
    #spark.writeStream.format("console").start()

    outStream = data_df \
        .writeStream \
        .format("console") \
        .trigger(continuous='1 second') \
        .start()

    #.writeStream.start()

    print('write data end ')
 
    
    #.load(file_name_input) \
    # .csv(file_name_input)  

    #data_df = spark \
    #  .readStream \
    #  .schema(userSchema) \
    #  .option("sep", ",") \
    #  .csv(file_name_input)  

    #data_df = spark.readStream.option(“sep”, “,”).option(“header”, “true”).schema(userSchema).csv(file_name_input)
 
    print('print data df')
    print(data_df)
    #display(data_df)
    #data_df.isStreaming()    # Returns True for DataFrames that have streaming sources
    print('print data schema')
    data_df.printSchema() 
     
    print('program done ')
    
    
    # diamonds = spark.read.format('csv').options(header='true', inferSchema='true').load('/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv')
    # display(diamonds)    


    # Split the lines into words
    #words = lines.select(
    #    # explode turns each item in an array into a separate row
    #    explode(
    #        split(lines.value, ' ')
    #    ).alias('word')
    #)

    # Generate running word count
    #wordCounts = words.groupBy('word').count()

    # Start running the query that prints the running counts to the console
    #query = wordCounts\
    #    .writeStream\
    #    .outputMode('complete')\
    #    .format('console')\
    #    .start()

    #query.awaitTermination()            
            
    # jsonSchema = StructType([ StructField("time", TimestampType(), True), StructField("action", StringType(), True) ])
    # staticInputDF = (
    #   spark
    #     .read
    #     .schema(jsonSchema)
    #     .json(inputPath)
    # )
    # display(staticInputDF)         
       
    # streamingCountsDF = (                 
    #   streamingInputDF
    #     .groupBy(
    #       streamingInputDF.action, 
    #       window(streamingInputDF.time, "1 hour"))
    #     .count()
    # )
    # streamingCountsDF.isStreaming
