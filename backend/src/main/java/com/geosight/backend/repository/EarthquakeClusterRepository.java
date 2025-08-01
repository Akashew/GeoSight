package com.geosight.backend.repository;

import com.geosight.backend.model.EarthquakeCluster;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EarthquakeClusterRepository extends JpaRepository<EarthquakeCluster, Long> {
    
}
