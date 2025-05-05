Open Terminal.

Run: java -version
If not downloaded download from: https://www.oracle.com/java/technologies/downloads/#jdk24-windows (remember over 3 billion devices run java)

(DO NOT change the names of the names of the code file)

Run the commands `javac HotelApp.java HotelClient.java`

In the same terminal run `rmiregistry`

Failsafe 1 - In case port taken error after running rmiregistry use in command porompt `netstat -aon | findstr :1098`

Failsafe 2 - (Use chatgpt and pray god it works and do not forget to "close the tab")

It shows 3-4 warnings ignore them (if too much errors then follow Failsafe 2)

in a new terminal run the command `java HotelApp.java`

In a new terminal run the command `java HotelClient.java`