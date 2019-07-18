package com.company;

public class truck {

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
