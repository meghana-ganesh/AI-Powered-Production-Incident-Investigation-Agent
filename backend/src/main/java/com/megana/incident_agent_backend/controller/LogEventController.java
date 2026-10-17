package com.megana.incident_agent_backend.controller;

import com.megana.incident_agent_backend.entity.LogEvent;
import com.megana.incident_agent_backend.repository.LogEventRepository;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.CrossOrigin;

import java.util.List;

@RestController
@RequestMapping("/api/logs")
@CrossOrigin(origins = "http://localhost:5173")
public class LogEventController {

    private final LogEventRepository logEventRepository;

    public LogEventController(LogEventRepository logEventRepository) {
        this.logEventRepository = logEventRepository;
    }

    @GetMapping
    public List<LogEvent> getLogs(
            @RequestParam(required = false) String service) {

        if (service != null) {
            return logEventRepository.findByService(service);
        }

        return logEventRepository.findAll();
    }

    @PostMapping
    public LogEvent createLog(@RequestBody LogEvent logEvent) {
        return logEventRepository.save(logEvent);
    }
}