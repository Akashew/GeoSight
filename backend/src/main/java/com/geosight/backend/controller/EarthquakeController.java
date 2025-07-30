package com.geosight.backend.controller;

import com.geosight.backend.model.Earthquake;
import com.geosight.backend.service.EarthquakeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/earthquakes")
public class EarthquakeController {

    private final EarthquakeService earthquakeService;

    @Autowired
    public EarthquakeController(EarthquakeService earthquakeService) {
        this.earthquakeService = earthquakeService;
    }

    @GetMapping
    public List<Earthquake> getAllEarthquakes() {
        return earthquakeService.getAllEarthquakes();
    }
}
