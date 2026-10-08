package com.careerlens.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.InputStream;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Serves the company vacancy catalogue (resources/vacancies.json), keyed by role id.
 * The role ids match the ones produced by the AI service (frontend, sales, ...).
 *
 * To plug in a live jobs API later, replace getForRole() and keep the same return shape.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class VacancyService {

    private final ObjectMapper objectMapper;
    private Map<String, List<Map<String, Object>>> catalogue = new HashMap<>();

    @PostConstruct
    void load() {
        try (InputStream in = new ClassPathResource("vacancies.json").getInputStream()) {
            catalogue = objectMapper.readValue(in, new TypeReference<Map<String, List<Map<String, Object>>>>() {});
            log.info("Loaded vacancy catalogue for {} roles", catalogue.size());
        } catch (Exception e) {
            log.error("Could not load vacancies.json: {}", e.getMessage());
        }
    }

    public List<Map<String, Object>> getForRole(String roleId) {
        return catalogue.getOrDefault(roleId, Collections.emptyList());
    }
}
