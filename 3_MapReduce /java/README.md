

### **Steps to Run:**

1. **Install Hadoop**: Follow the installation guide for setting up Hadoop on your system.
   
2. **Create `sample.txt` file**: In your home folder, create the file `sample.txt` with the text you want to process.

3. **Create the Project in Eclipse**:
   - Create a new Java project named `exp5a` in Eclipse.
   - Create three classes: `CharMap`, `CharReduce`, and `CharCount`.

4. **Import Necessary JAR Files**:
   - Import the required Hadoop libraries into the project (`hadoop-mapreduce-client-core-2.7.1.jar`, `hadoop-common-2.7.1.jar`, `commons-cli-1.2.jar`).

5. **Write the MapReduce Code**: Add the code for `CharMap`, `CharReduce`, and `CharCount` in the respective classes.

6. **Export the JAR File**:
   - Right-click on the `exp5a` project in Eclipse, then export the project as a JAR file (`exp5a.jar`).
   - Save the JAR file in your home directory.

7. **Start Hadoop**:
   - Start the NameNode and DataNode daemons with the following command:
     ```bash
     ~/hadoop/sbin/start-dfs.sh
     ```

8. **Make HDFS Directories**:
   - Make the required directories for input and output in HDFS:
     ```bash
     ~/hadoop/bin/hdfs dfs -mkdir /user
     ~/hadoop/bin/hdfs dfs -mkdir /user/your_user_name
     ```

9. **Put `sample.txt` in HDFS**:
   - Upload the `sample.txt` file to HDFS:
     ```bash
     ~/hadoop/bin/hdfs dfs -put ~/sample.txt input_data
     ```

10. **Run the MapReduce Job**:
    - Execute the MapReduce job:
      ```bash
      ~/hadoop/bin/hadoop jar ~/exp5a.jar input_data output_data
      ```

11. **Check the Output**:
    - View the output of the MapReduce job:
      ```bash
      ~/hadoop/bin/hdfs dfs -cat output_data/*
      ```

12. **Clean Up**:
    - After the task is complete, remove the input and output data from HDFS:
      ```bash
      ~/hadoop/bin/hdfs dfs -rm -r input_data output_data
      ```

13. **Stop Hadoop**:
    - Stop the Hadoop daemons:
      ```bash
      ~/hadoop/sbin/stop-dfs.sh
      ```

This process allows you to run a distributed character counting MapReduce job using Hadoop.