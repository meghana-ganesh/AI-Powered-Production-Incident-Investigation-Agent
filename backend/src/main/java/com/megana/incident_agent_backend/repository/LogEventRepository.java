package com.megana.incident_agent_backend.repository;

import com.megana.incident_agent_backend.entity.LogEvent;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDateTime;
import java.util.List;

public interface LogEventRepository extends JpaRepository<LogEvent, Long> {

    List<LogEvent> findByService(String service);

    List<LogEvent> findByServiceAndTimestampBetween(
            String service,
            LocalDateTime start,
            LocalDateTime end
    );

    List<LogEvent> findByLevel(String level);
}
