package com.geosight.backend.controller;

import com.geosight.backend.model.Earthquake;
import com.geosight.backend.service.EarthquakeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

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


    @GetMapping("/search")
    public Page<Earthquake> searchEarthquakes(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(defaultValue = "0.0") double minMagnitude,
        @RequestParam(defaultValue = "10.0") double maxMagnitude,
        @RequestParam(defaultValue = "") String place
    ) {
        Pageable pageable = PageRequest.of(page, size);
        return earthquakeService.getFilteredEarthquakes(minMagnitude, maxMagnitude, place, pageable);
    }

    @GetMapping("/cluster/{clusterId}")
    public Page<Earthquake> getEarthquakesByClusterId(
        @PathVariable Long clusterId,
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size
    ) {
        Pageable pageable = PageRequest.of(page, size);
        return earthquakeService.getEarthquakesByClusterId(clusterId, pageable);
    }



}
