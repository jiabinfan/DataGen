package com.company;

//Imports
import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;
public class Main {

    //Manipulable Variables
    private static int busWeight = 0;
    private static int maxBike = 15;
    private static double depotXPos = 34.28037084;
    private static double depotYPos = 108.9691212;
    private static int startingBikes = 10;
    private static String fileName = "/home/agao/ALL_DATA_7-1000-110/";
    private static int totNumb = 999;

    //Global Variables
    private static ArrayList<Station> stations = new ArrayList<>();
    private static ArrayList<Station> defStations = new ArrayList<>();
    private static truck Truck = new truck(depotXPos, depotYPos, startingBikes);
    private static double totDist = 0;
    private static double totEmissions = 0;
    private static int numStations;

    public static Scanner wordScan = new Scanner(System.in);
    public static Scanner numScan = new Scanner(System.in);

    private static ArrayList<Double> allDist = new ArrayList<>();
    private static ArrayList<Double> allEmis = new ArrayList<>();

    public static void main(String[] args) {


            for (int i = 0; i <= totNumb; i++) {

                totDist = 0;
                totEmissions = 0;
                int temp = importer(i);
                //System.out.println();
                if (startingBikes == 0) {
                    if (temp < 0) {
                        Truck.setBike(Math.abs(temp));
                    } else {
                        Truck.setBike(0);
                    }
                } else {
                    if (temp < 0) {
                        Truck.setBike(Math.abs(temp) + startingBikes);
                    } else {
                        Truck.setBike(startingBikes);
                    }
                }
                //Truck.setBike(20);
                Truck.cngPos(34.275555, 108.955555);
                //Calculate Stations

                while (numStations > 0) {
                    calcDist();
                    goStation();

                }
                calcPrint();

                System.out.println(i);
            }
            System.out.println();
            System.out.println("###############################################################################");
            System.out.println("                 DONE                                      DONE          ");
        System.out.println();

            csvWrite();
            finalPrint();

    }//End Main

    //Import distances form csv
    private static int importer(int num) {
        String line;

        int totBike = 0;
        int nameNum = 1;

        //String fileName = "stations12.csv";

        String FileName = fileName + num + ".csv";

        try {
            BufferedReader reader = new BufferedReader(new FileReader(FileName));

            while ((line = reader.readLine()) != null) {
                String[] temp = line.split(",");
                //Sort to ArrayLists
                if (Integer.parseInt(temp[2]) < 0) {
                    //int num = Integer.parseInt(temp[2]);
                    defStations.add(new Station(Double.parseDouble(temp[0]), Double.parseDouble(temp[1]), /*randGen()*/ Integer.parseInt(temp[2]), ("" + nameNum)));

                } else {
                    stations.add(new Station(Double.parseDouble(temp[0]), Double.parseDouble(temp[1]),  /*randGen()*/ Integer.parseInt(temp[2]), ("" + nameNum)));
                }

                //Calculate Total Bikes
                totBike += Integer.parseInt(temp[2]);
                nameNum++;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        //Define number of stations
        numStations = defStations.size() + stations.size();
        return totBike;
    }//End importer

    private static void csvWrite() {
        try (PrintWriter writer = new PrintWriter( new File("/home/agao/EXPORT/out.csv"))){

            StringBuilder sb = new StringBuilder();

            for (int i = 0; i < allDist.size(); i++) {
                sb.append(allDist.get(i));
                sb.append(",");
                sb.append(allEmis.get(i));
                sb.append("\n");
            }

            writer.write(sb.toString());

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //Calculate Distances
    private static void calcDist() {
        //Cycle through positive stations
        for (int i = 0; i < stations.size(); i++) {
            setDist(i, stations);
        }
        //Cycle through deficit stations
        for (int i = 0; i < defStations.size(); i++) {
            setDist(i, defStations);
        }
        //Sort the ArrayList
        sorter();
    }//End calcDist
    private static void setDist( int i, ArrayList<Station> tempList) {
        double s1 = tempList.get(i).getxPos() - Truck.getxPos();
        double s2 = tempList.get(i).getyPos() - Truck.getyPos();

        tempList.get(i).setNextDist(Math.sqrt((s1 * s1) + (s2 * s2)));
    }//End setDist

    //Sort ArrayList
    private static void sorter() {
        //Sort stations
        Collections.sort(defStations);
        Collections.sort(stations);
    }//End sorter

    //Go to stations
    private static void goStation() {
        boolean isDropOff = false;

        //Find Stations with deficit and go to closest that satisfies conditions
        for (int i = 0; i < defStations.size(); i++) {
            if (Math.abs(defStations.get(i).getNumBikes()) <= Truck.getBikes()){
                isDropOff = true;

                doStationCalc(defStations, i, true);

                break;
            }
        }

        //Find surplus stations when no stations with deficits are available
        if(!isDropOff){
            for (int i = 0; i < stations.size(); i++) {
                if (Truck.getBikes() + stations.get(i).getNumBikes() <= maxBike){

                    doStationCalc(stations, i, false);

                    break;
                }
            }
        }
    }//End goStation
    private static void doStationCalc(ArrayList<Station> temp, int i, boolean isDef) {
        numStations--;
        totDist += temp.get(i).getNextDist();
        totEmissions += (temp.get(i).getNextDist()) * (Truck.getBikes() + busWeight);

        //int truckBikes = Truck.getBikes();

        Truck.cngPos(temp.get(i).getxPos(), temp.get(i).getyPos());
        Truck.cngBike(temp.get(i).getNumBikes());
        if(isDef) {
            //System.out.println(defStations.get(i) + ", " + truckBikes);
            defStations.remove(i);
        } else {
            //System.out.println(stations.get(i) + ", " + truckBikes);
            stations.remove(i);
        }
    }//End doStationCalc

    //Final info print
    private static void calcPrint() {
        double s1 = depotXPos - Truck.getxPos();
        double s2 = depotYPos - Truck.getyPos();

        double finalDist = (Math.sqrt((s1 * s1) + (s2 * s2)));

        totDist += finalDist;
        totEmissions += finalDist * (Truck.getBikes() + busWeight);

        allDist.add(totDist);
        allEmis.add(totEmissions);

        //System.out.println(totDist);
        //System.out.println(totEmissions) ;
    }// End CalcPrint

    private static void finalPrint() {
        System.out.println("Distance");
        double avg = 0;
        for (int i = 0; i < allDist.size(); i++) {
            avg += allDist.get(i);
        }
        System.out.println(avg/allDist.size());
        System.out.println();
        avg = 0;
        System.out.println("Emissions");
        for (int i = 0; i < allEmis.size(); i++) {
            avg += allEmis.get(i);
        }
        System.out.println(avg/allEmis.size());
    }
}//End Class

class Station implements Comparable<Station> {

    private double xPos;
    private double yPos;
    private int numBikes;
    private double nextDist;
    private String name;

    public Station(double x, double y, int num, String n){
        xPos = x;
        yPos = y;
        numBikes = num;
        name = n;
    }

    public double getxPos() {
        return xPos;
    }

    public double getyPos() {
        return yPos;
    }

    public int getNumBikes() {
        return numBikes;
    }

    public void setNextDist(double d) {
        nextDist =  d;
    }

    public double getNextDist(){
        return nextDist;
    }

    @Override
    public int compareTo(Station compareStation){
        if(this.getNextDist()>compareStation.getNextDist()){
            return 1;
        } else if (this.getNextDist() == compareStation.getNextDist()) {
            return 0;
        } else {
            return -1;
        }
    }

    @Override
    public String toString() {
        return name;
    }

    /*public String toString() {
        return nextDist + "";
    }*/

}

class truck {

    private double xPos;
    private double yPos;
    private int bikes;

    public truck(double x, double y, int b){
        xPos = x;
        bikes = b;
        yPos = y;
    }

    public double getxPos() {
        return xPos;
    }

    public double getyPos() {
        return yPos;
    }

    public int getBikes() {
        return bikes;
    }

    public void cngBike(int val){
        bikes += val;
    }

    public void setBike(int val){
        bikes = val;
    }

    public void cngPos(double x, double y){
        xPos = x;
        yPos = y;
    }
}