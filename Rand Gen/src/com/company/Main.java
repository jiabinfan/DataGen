package com.company;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;

public class Main {

    public static ArrayList<station> allStations = new ArrayList<>();

    //public static ArrayList<Integer> totSum = new ArrayList<>();

    private static String fileStructure = "/home/agao/ALL_DATA_25-100000/";
    //private static String inFile = "110_Cord.csv";
    public static String inFile = "25_Cord.csv";
    private static int numGen = 100000;

    public static void main(String[] args) {

        importer();


        /*for (int i = 0; i < 3; i++) {
            Collections.shuffle(totSum);
            csvWrite(i);
        }*/

        int numCorr = 0;
        while(numCorr < numGen) {

            int totalSum = 0;

            for (int i = 0; i < allStations.size(); i++) {

                int randNum = 0;

                while(true){
                    randNum = ((int)(Math.random() * 50) - 25);
                    if(randNum != 0){
                        break;
                    }
                }

                allStations.get(i).setNumb(randNum);


                totalSum += allStations.get(i).getNumb();
            }

            if (totalSum >= -5 && totalSum <= 5) {
                csvWrite(numCorr);
                System.out.println(numCorr);
                numCorr++;
            }
        }
    }

    private static void importer() {
        String line;

        try {
            BufferedReader reader = new BufferedReader(new FileReader(inFile));

            while ((line = reader.readLine()) != null) {
                String[] temp = line.split(",");
                //Sort to ArrayLists

                    allStations.add(new station(Double.parseDouble(temp[0]), Double.parseDouble(temp[1])));
                    //totSum.add(Integer.parseInt(temp[2]));

            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void csvWrite(int z) {
        try (PrintWriter writer = new PrintWriter( new File(fileStructure + z + ".csv"))){

            StringBuilder sb = new StringBuilder();

            for (int i = 0; i < allStations.size(); i++) {
                sb.append(allStations.get(i).toString());
                //sb.append(",");
                //sb.append(totSum.get(i));
                sb.append("\n");
            }

            writer.write(sb.toString());

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class station {

    double xPos;
    double yPos;
    int numb;

    public station(double xPos, double yPos) {
        this.xPos = xPos;
        this.yPos = yPos;
    }

    public int getNumb() {
        return numb;
    }

    public void setNumb(int numb) {
        this.numb = numb;
    }

    @Override
    public String toString() {
        return xPos +
                "," + yPos + "," + numb;
    }
}
