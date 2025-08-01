package com.geosight.backend.controller;

import com.geosight.backend.model.EarthquakeCluster;
import com.geosight.backend.service.EarthquakeClusterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

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
    public EarthquakeCluster getClusterById(@PathVariable Integer id) {
        return service.getClusterById(id);
    }

    @PostMapping
    public EarthquakeCluster createCluster(@RequestBody EarthquakeCluster cluster) {
        return service.createCluster(cluster);
    }

    @PutMapping("/{id}")
    public EarthquakeCluster updateCluster(@PathVariable Integer id, @RequestBody EarthquakeCluster cluster) {
        return service.updateCluster(id, cluster);
    }

    @DeleteMapping("/{id}")
    public void deleteCluster(@PathVariable Integer id) {
        service.deleteCluster(id);
    }

    @GetMapping("/search")
    public Page<EarthquakeCluster> searchClusters(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(required = false) Double minLat,
        @RequestParam(required = false) Double maxLat,
        @RequestParam(required = false) Double minLon,
        @RequestParam(required = false) Double maxLon,
        @RequestParam(required = false) Integer minSize,
        @RequestParam(required = false) Integer maxSize
    ) {
        Pageable pageable = PageRequest.of(page, size);
        return service.getFilteredClusters(minLat, maxLat, minLon, maxLon, minSize, maxSize, pageable);
    }
}
