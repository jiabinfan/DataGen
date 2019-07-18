package com.company;

public class Station implements Comparable<Station> {

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
