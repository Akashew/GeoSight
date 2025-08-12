package com.geosight.backend.controller;

import com.geosight.backend.model.EarthquakeCluster;
import com.geosight.backend.model.Earthquake;
import com.geosight.backend.service.EarthquakeClusterService;
import com.geosight.backend.service.EarthquakeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import java.util.List;

@RestController
@RequestMapping("/api/earthquake_clusters")
public class EarthquakeClusterController {

    private final EarthquakeClusterService clusterService;
    private final EarthquakeService earthquakeService;

    @Autowired
    public EarthquakeClusterController(EarthquakeClusterService clusterService, EarthquakeService earthquakeService) {
        this.clusterService = clusterService;
        this.earthquakeService = earthquakeService;
    }

    @GetMapping
    public List<EarthquakeCluster> getAllClusters() {
        return clusterService.getAllClusters();
    }

    @GetMapping("/{id}")
    public EarthquakeCluster getClusterById(@PathVariable Integer id) {
        return clusterService.getClusterById(id);
    }

    @PostMapping
    public EarthquakeCluster createCluster(@RequestBody EarthquakeCluster cluster) {
        return clusterService.createCluster(cluster);
    }

    @PutMapping("/{id}")
    public EarthquakeCluster updateCluster(@PathVariable Integer id, @RequestBody EarthquakeCluster cluster) {
        return clusterService.updateCluster(id, cluster);
    }

    @DeleteMapping("/{id}")
    public void deleteCluster(@PathVariable Integer id) {
        clusterService.deleteCluster(id);
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
        return clusterService.getFilteredClusters(minLat, maxLat, minLon, maxLon, minSize, maxSize, pageable);
    }
    
    @GetMapping("/{clusterId}/earthquakes")
    public Page<Earthquake> getEarthquakesByCluster(
        @PathVariable Long clusterId,
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size
    ) {
        Pageable pageable = PageRequest.of(page, size);
        return earthquakeService.getEarthquakesByClusterId(clusterId, pageable);
    }
}
