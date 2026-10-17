package com.megana.incident_agent_backend.controller;

import com.megana.incident_agent_backend.entity.DeploymentEvent;
import com.megana.incident_agent_backend.repository.DeploymentEventRepository;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.CrossOrigin;

import java.util.List;

@RestController
@RequestMapping("/api/deployments")
@CrossOrigin(origins = "http://localhost:5173")
public class DeploymentEventController {

    private final DeploymentEventRepository repository;

    public DeploymentEventController(DeploymentEventRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<DeploymentEvent> getDeployments(
            @RequestParam(required = false) String service) {

        if (service != null) {
            return repository.findByServiceOrderByTimestampDesc(service);
        }

        return repository.findAll();
    }

    @PostMapping
    public DeploymentEvent createDeployment(
            @RequestBody DeploymentEvent deployment) {

        return repository.save(deployment);
    }
}