package com.megana.incident_agent_backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = "com.megana.incident_agent_backend")
public class IncidentAgentBackendApplication {

	public static void main(String[] args) {
		SpringApplication.run(IncidentAgentBackendApplication.class, args);
	}

}
