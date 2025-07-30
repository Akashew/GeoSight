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

    public Earthquake getEarthquakeById(String id) {
        return earthquakeRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Earthquake not found with id: " + id));
    }

    public Earthquake saveEarthquake(Earthquake earthquake) {
        return earthquakeRepository.save(earthquake);
    }

    public void deleteEarthquake(String id) {
        if (!earthquakeRepository.existsById(id)) {
            throw new RuntimeException("Earthquake not found with id " + id);
        }
        earthquakeRepository.deleteById(id);
    }

    public Earthquake updateEarthquake(String id, Earthquake updatedEarthquake) {
        Earthquake existingEarthquake = earthquakeRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Earthquake not found with id: " + id));
    
        existingEarthquake.setTime(updatedEarthquake.getTime());
        existingEarthquake.setLatitude(updatedEarthquake.getLatitude());
        existingEarthquake.setLongitude(updatedEarthquake.getLongitude());
        existingEarthquake.setDepth(updatedEarthquake.getDepth());
        existingEarthquake.setMagnitude(updatedEarthquake.getMagnitude());
        existingEarthquake.setPlace(updatedEarthquake.getPlace());

        return earthquakeRepository.save(existingEarthquake);
    }



    // Optional: Add other methods like getById, filterByMagnitude, etc.
}

