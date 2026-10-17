package com.megana.incident_agent_backend.controller;

import com.megana.incident_agent_backend.entity.DeploymentEvent;
import com.megana.incident_agent_backend.entity.Incident;
import com.megana.incident_agent_backend.entity.LogEvent;
import com.megana.incident_agent_backend.entity.MetricEvent;
import com.megana.incident_agent_backend.repository.DeploymentEventRepository;
import com.megana.incident_agent_backend.repository.IncidentRepository;
import com.megana.incident_agent_backend.repository.LogEventRepository;
import com.megana.incident_agent_backend.repository.MetricEventRepository;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.CrossOrigin;

@RestController
@RequestMapping("/api/incidents")
@CrossOrigin(origins = "http://localhost:5173")
public class InvestigationController {

    private final IncidentRepository incidentRepository;
    private final LogEventRepository logRepository;
    private final MetricEventRepository metricRepository;
    private final DeploymentEventRepository deploymentRepository;

    public InvestigationController(
            IncidentRepository incidentRepository,
            LogEventRepository logRepository,
            MetricEventRepository metricRepository,
            DeploymentEventRepository deploymentRepository) {

        this.incidentRepository = incidentRepository;
        this.logRepository = logRepository;
        this.metricRepository = metricRepository;
        this.deploymentRepository = deploymentRepository;
    }

    @GetMapping("/{id}/investigation-data")
    public Map<String, Object> getInvestigationData(
            @PathVariable Long id) {

        Incident incident = incidentRepository.findById(id)
                .orElseThrow(() ->
                        new RuntimeException("Incident not found"));

        String service = incident.getService();

        List<LogEvent> logs =
                logRepository.findByService(service);

        List<MetricEvent> metrics =
                metricRepository.findByService(service);

        List<DeploymentEvent> deployments =
                deploymentRepository.findByServiceOrderByTimestampDesc(service);

        Map<String, Object> result = new HashMap<>();

        result.put("incident", incident);
        result.put("logs", logs);
        result.put("metrics", metrics);
        result.put("deployments", deployments);

        return result;
    }
}