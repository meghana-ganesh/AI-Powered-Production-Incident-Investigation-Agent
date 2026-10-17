package com.megana.incident_agent_backend.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@Entity
@Table(name = "metric_events")
public class MetricEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private LocalDateTime timestamp;

    @Column(nullable = false)
    private String service;

    @Column(nullable = false)
    private String metric;

    @Column(name = "metric_value")
    private Double value;

    private String unit;
}