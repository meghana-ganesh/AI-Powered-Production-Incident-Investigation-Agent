package com.megana.incident_agent_backend.repository;

import com.megana.incident_agent_backend.entity.MetricEvent;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDateTime;
import java.util.List;

public interface MetricEventRepository extends JpaRepository<MetricEvent, Long> {

    List<MetricEvent> findByService(String service);

    List<MetricEvent> findByServiceAndTimestampBetween(
            String service,
            LocalDateTime start,
            LocalDateTime end
    );

    List<MetricEvent> findByServiceAndMetric(
            String service,
            String metric
    );
}