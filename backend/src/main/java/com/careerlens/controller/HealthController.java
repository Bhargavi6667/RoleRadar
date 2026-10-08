package com.careerlens.controller;

import com.careerlens.client.AiServiceClient;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/health")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class HealthController {

    private final AiServiceClient aiServiceClient;

    @GetMapping
    public ResponseEntity<Map<String, Object>> getHealth() {
        Map<String, Object> health = new HashMap<>();
        health.put("backend_status", "UP");
        health.put("timestamp", LocalDateTime.now().toString());

        Map<String, Object> aiHealth = aiServiceClient.checkHealth();
        health.put("ai_service", aiHealth);

        return ResponseEntity.ok(health);
    }
}
