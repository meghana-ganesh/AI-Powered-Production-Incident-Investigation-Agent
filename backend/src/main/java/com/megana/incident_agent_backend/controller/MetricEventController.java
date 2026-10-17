package com.megana.incident_agent_backend.controller;

import com.megana.incident_agent_backend.entity.MetricEvent;
import com.megana.incident_agent_backend.repository.MetricEventRepository;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.CrossOrigin;

import java.util.List;

@RestController
@RequestMapping("/api/metrics")
@CrossOrigin(origins = "http://localhost:5173")
public class MetricEventController {

    private final MetricEventRepository repository;

    public MetricEventController(MetricEventRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<MetricEvent> getMetrics(
            @RequestParam(required = false) String service) {

        if (service != null) {
            return repository.findByService(service);
        }

        return repository.findAll();
    }

    @PostMapping
    public MetricEvent createMetric(@RequestBody MetricEvent metric) {
        return repository.save(metric);
    }
}