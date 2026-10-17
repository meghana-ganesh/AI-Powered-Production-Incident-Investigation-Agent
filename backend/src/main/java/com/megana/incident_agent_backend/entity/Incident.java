package com.megana.incident_agent_backend.entity;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Table(name = "incidents")
@Getter
@Setter
public class Incident 
{
    @Id 
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false)
    private String service;

    @Column(length = 2000)
    private String description;

    private String severity;

    private String status;

    public Incident() {
    }
    public Incident(String title, String service, String description, String severity, String status) {
        this.title = title;
        this.service = service;
        this.description = description;
        this.severity = severity;
        this.status = status;
    }
}
