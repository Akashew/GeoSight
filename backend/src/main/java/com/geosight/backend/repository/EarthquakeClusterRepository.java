package com.geosight.backend.repository;

import com.geosight.backend.model.EarthquakeCluster;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface EarthquakeClusterRepository extends JpaRepository<EarthquakeCluster, Integer>, JpaSpecificationExecutor<EarthquakeCluster> {
}
