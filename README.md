Environment Setup.
--------------------------------------
l�gg till systemvariabler.

kontrollpanelen -> System och s�kerhet -> System -> Avancerade systeminst�llningar -> Milj�variabler

Systemvariabler Ny...

JAVA_HOME : /path/to/java/jdk
M2_HOME : /path/to/apache-maven-3.3.9
MAVEN_HOME : /path/to/apache-maven-3.3.9

MAHOUT_HOME : /path/to/mahout
MAHOUT_LOCAL : true

Redigera Path.
l�gg till %M2_HOME%\bin

How To Run Flink
-------------------------------------
run start-local.bat
for webinterface go to http://localhost:8081/

for examples on how to run commands on flink se link:
https://ci.apache.org/projects/flink/flink-docs-release-1.2/setup/cli.html