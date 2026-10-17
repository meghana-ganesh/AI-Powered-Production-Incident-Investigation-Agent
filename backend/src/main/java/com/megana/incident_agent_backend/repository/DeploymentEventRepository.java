package com.megana.incident_agent_backend.repository;

import com.megana.incident_agent_backend.entity.DeploymentEvent;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface DeploymentEventRepository
        extends JpaRepository<DeploymentEvent, Long> {

    List<DeploymentEvent> findByService(String service);

    List<DeploymentEvent> findByServiceOrderByTimestampDesc(String service);
}