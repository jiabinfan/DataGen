package com.company;

public class station {

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
