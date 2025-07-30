package com.geosight.backend.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "earthquakes")
public class Earthquake {
    @Id
    private String id;
    private String time;
    private double latitude;
    private double longitude;
    private double depth;
    private double magnitude;
    private String place;

    
    public String getId() { 
        return id; 
    }

    public void setId(String id) { 
        this.id = id; 
    }

    public String getTime() { 
        return time; 
    }

    public void setTime(String time) { 
        this.time = time; 
    }

    public double getLatitude() { 
        return latitude; 
    }

    public void setLatitude(double latitude) { 
        this.latitude = latitude; 
    }

    public double getLongitude() { 
        return longitude; 
    }

    public void setLongitude(double longitude) { 
        this.longitude = longitude; 
    }

    public double getDepth() { 
        return depth; 
    }

    public void setDepth(double depth) { 
        this.depth = depth; 
    }

    public double getMagnitude() { 
        return magnitude; 
    }

    public void setMagnitude(double magnitude) { 
        this.magnitude = magnitude; 
    }

    public String getPlace() { 
        return place; 
    }

    public void setPlace(String place) { 
        this.place = place; 
    }
}
