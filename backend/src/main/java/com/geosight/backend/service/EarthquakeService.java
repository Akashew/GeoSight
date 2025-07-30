package com.geosight.backend.service;

import com.geosight.backend.model.Earthquake;
import com.geosight.backend.repository.EarthquakeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EarthquakeService {

    private final EarthquakeRepository earthquakeRepository;

    @Autowired
    public EarthquakeService(EarthquakeRepository earthquakeRepository) {
        this.earthquakeRepository = earthquakeRepository;
    }

    public List<Earthquake> getAllEarthquakes() {
        return earthquakeRepository.findAll();
    }

    // Optional: Add other methods like getById, filterByMagnitude, etc.
}

