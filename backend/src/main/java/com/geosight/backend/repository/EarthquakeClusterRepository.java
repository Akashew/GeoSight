package com.geosight.backend.repository;

import com.geosight.backend.model.EarthquakeCluster;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface EarthquakeClusterRepository extends JpaRepository<EarthquakeCluster, Integer> {

    Page<EarthquakeCluster> findByLatitudeBetweenAndLongitudeBetweenAndClusterSizeBetween(
        double minLat, double maxLat,
        double minLon, double maxLon,
        int minSize, int maxSize,
        Pageable pageable
    );
}
