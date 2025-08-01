package com.geosight.backend.controller;

import com.geosight.backend.model.EarthquakeCluster;
import com.geosight.backend.service.EarthquakeClusterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/earthquake_clusters")
public class EarthquakeClusterController {

    private final EarthquakeClusterService service;

    @Autowired
    public EarthquakeClusterController(EarthquakeClusterService service) {
        this.service = service;
    }

    @GetMapping
    public List<EarthquakeCluster> getAllClusters() {
        return service.getAllClusters();
    }

    @GetMapping("/{id}")
    public EarthquakeCluster getClusterById(@PathVariable Long id) {
        return service.getClusterById(id);
    }

    @PostMapping
    public EarthquakeCluster createCluster(@RequestBody EarthquakeCluster cluster) {
        return service.createCluster(cluster);
    }

    @PutMapping("/{id}")
    public EarthquakeCluster updateCluster(@PathVariable Long id, @RequestBody EarthquakeCluster updatedCluster) {
        return service.updateCluster(id, updatedCluster);
    }

    @DeleteMapping("/{id}")
    public void deleteCluster(@PathVariable Long id) {
        service.deleteCluster(id);
    }
}
