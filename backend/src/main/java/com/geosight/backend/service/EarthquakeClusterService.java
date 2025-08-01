package com.geosight.backend.service;

import com.geosight.backend.model.EarthquakeCluster;
import com.geosight.backend.repository.EarthquakeClusterRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;

import jakarta.persistence.criteria.Predicate;
import java.util.ArrayList;
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

    public EarthquakeCluster getClusterById(Integer id) {
        return repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Cluster not found with id: " + id));
    }

    public EarthquakeCluster createCluster(EarthquakeCluster cluster) {
        return repository.save(cluster);
    }

    public EarthquakeCluster updateCluster(Integer id, EarthquakeCluster updatedCluster) {
        EarthquakeCluster existing = repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Cluster not found with id: " + id));
        existing.setLatitude(updatedCluster.getLatitude());
        existing.setLongitude(updatedCluster.getLongitude());
        existing.setClusterSize(updatedCluster.getClusterSize());
        return repository.save(existing);
    }

    public void deleteCluster(Integer id) {
        if (!repository.existsById(id)) {
            throw new RuntimeException("Cluster not found with id: " + id);
        }
        repository.deleteById(id);
    }

    public Page<EarthquakeCluster> getFilteredClusters(
        Double minLat, Double maxLat,
        Double minLon, Double maxLon,
        Integer minSize, Integer maxSize,
        Pageable pageable
    ) {
        Specification<EarthquakeCluster> spec = (root, query, cb) -> {
            List<Predicate> predicates = new ArrayList<>();

            if (minLat != null) predicates.add(cb.greaterThanOrEqualTo(root.get("latitude"), minLat));
            if (maxLat != null) predicates.add(cb.lessThanOrEqualTo(root.get("latitude"), maxLat));
            if (minLon != null) predicates.add(cb.greaterThanOrEqualTo(root.get("longitude"), minLon));
            if (maxLon != null) predicates.add(cb.lessThanOrEqualTo(root.get("longitude"), maxLon));
            if (minSize != null) predicates.add(cb.greaterThanOrEqualTo(root.get("clusterSize"), minSize));
            if (maxSize != null) predicates.add(cb.lessThanOrEqualTo(root.get("clusterSize"), maxSize));

            return cb.and(predicates.toArray(new Predicate[0]));
        };

        return repository.findAll(spec, pageable);
    }
}
