package com.geosight.backend.service;

import com.geosight.backend.model.EarthquakeCluster;
import com.geosight.backend.repository.EarthquakeClusterRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EarthquakeClusterService {

    private final EarthquakeClusterRepository repository;

    @Autowired
    public EarthquakeClusterService(EarthquakeClusterRepository repository) {
        this.repository = repository;
    }

    public List<EarthquakeCluster> getAllClusters() {
        return repository.findAll();
    }

    public EarthquakeCluster getClusterById(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Cluster not found with id " + id));
    }

    public EarthquakeCluster createCluster(EarthquakeCluster cluster) {
        return repository.save(cluster);
    }

    public EarthquakeCluster updateCluster(Long id, EarthquakeCluster updatedCluster) {
        EarthquakeCluster existing = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Cluster not found with id " + id));

        existing.setLatitude(updatedCluster.getLatitude());
        existing.setLongitude(updatedCluster.getLongitude());
        existing.setClusterSize(updatedCluster.getClusterSize());

        return repository.save(existing);
    }

    public void deleteCluster(Long id) {
        if (!repository.existsById(id)) {
            throw new RuntimeException("Cluster not found with id " + id);
        }
        repository.deleteById(id);
    }
}
