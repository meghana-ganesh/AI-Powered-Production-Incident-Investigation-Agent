package com.megana.incident_agent_backend.repository;
import com.megana.incident_agent_backend.entity.Incident;
import org.springframework.data.jpa.repository.*;

public interface IncidentRepository extends JpaRepository<Incident, Long> 
{

}
