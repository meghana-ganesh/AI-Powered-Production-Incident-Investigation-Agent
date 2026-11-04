package com.megana.incident_agent_backend.service;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;
import org.springframework.web.server.ResponseStatusException;

@Service
public class InvestigationAiService 
{
    private final RestClient restClient;
    public InvestigationAiService(
        RestClient.Builder restClientBuilder,
        @Value ("${ai.service.url}") String aiServiceUrl){
        this.restClient = restClientBuilder
            .baseUrl(aiServiceUrl)
            .build();
        }
    public Map<String,Object> investigate(Long incidentId){
        try{
            return restClient.post()
                .uri("/investigate/{incidentId}", incidentId)
                .retrieve()
                .body(Map.class);
        }
        catch (RestClientException e){
            throw new ResponseStatusException(HttpStatus.BAD_GATEWAY, "AI Incident Service failed.Please try again later.", e);
        }
    }
}
