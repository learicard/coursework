Here's is some code techniques for debuging Python streaming.

# Programs using map/reduce is notoriously difficult to debug,

# especially because Hadoop is managing the execution and standard error/output files

#

# There are several approaches you can use, some of which depend on your Hadoop set up, like finding the 'userlog' files and looking for standard error/output files.

# Here is perhaps an old-fashioned approach, but one that can be very informative.

# In your program you can print debugging information to a file that is in a shared location, which means you have to name the file differently for each map or reduce program. Hopefully, if your program is crashing, this will help you pinpoint the problem. As always, when debugging, you might want to run tests with a little bit of data.

#Here are the steps using Python:

1. Hadoop has some environmental variables you can use, such as task id. Before your main loop enter these lines:

    import os
    myid=os.environ["mapred_tip_id"]
    # for testing a script in a unix pipe, just set to str e.g., `myid='pipe_test'`

2. Open a file for writing. Cloudera VM lets tasks write to `/tmp`, other installations might have better place to write to. Somewhere in your code add some debug statements, this can help show how the program is doing and where it might be crashing, such as:

    mylog=open("/tmp/mymaplog"+myid,"w")
    for line in sys.stdin:
        #sys.stdin call 'sys' to read a line from standard input
        ....
        mylog.write(line)
        ...
        mylog.write(key)

    mylog.close()

3. Now you can look at the /tmp/mylog* files, try

    ls -ldth /tmp/mymaplog*
    more /tmp/mymaplog__ # where the __ is the log file you want to see.

4. Some people have found that running dos2unix on the wordcount_*.py files helps ensure the text is converted properly. Unix vs Dos necessary newline characters can sometimes mess things up.

5. http://allthingshadoop.com/2011/12/16/simple-hadoop-streaming-tutorial-using-joins-and-keys-with-python/

6. Hue will make some map/reduce job log information available. First, you open your browser and login into the Hue. If you use the cloudera-quickstart-vm, the link looks like this: http://quickstart.cloudera:8888/jobbrowser/. Second, you click one of the failed jobs, select the logs and go to the stderr tab.


