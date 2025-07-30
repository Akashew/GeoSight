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

    @GetMapping("/{id}")
    public Earthquake getEarthquakeById(@PathVariable String id) {
        return earthquakeService.getEarthquakeById(id);
    }

    @PostMapping
    public Earthquake createEarthquake(@RequestBody Earthquake earthquake) {
        return earthquakeService.saveEarthquake(earthquake);
    }

    @DeleteMapping("/{id}")
    public void deleteEarthquake(@PathVariable String id) {
        earthquakeService.deleteEarthquake(id);
    }

    @PutMapping("/{id}")
    public Earthquake updateEarthquake(@PathVariable String id, @RequestBody Earthquake earthquake) {
        return earthquakeService.updateEarthquake(id, earthquake);
    }



}
