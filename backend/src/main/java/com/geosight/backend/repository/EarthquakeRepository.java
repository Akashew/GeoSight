package com.geosight.backend.repository;

import com.geosight.backend.model.Earthquake;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;


@Repository
public interface EarthquakeRepository extends JpaRepository<Earthquake, String>{

    Page<Earthquake> findByMagnitudeBetweenAndPlaceContainingIgnoreCase(
        double minMagnitude, double maxMagnitude, String place, Pageable pageable
    );

    Page<Earthquake> findByClusterId(Long clusterId, Pageable pageable);
    
}
