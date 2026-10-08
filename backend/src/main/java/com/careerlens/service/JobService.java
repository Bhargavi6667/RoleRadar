package com.careerlens.service;

import com.careerlens.client.AiServiceClient;
import com.careerlens.dto.JobCreateRequest;
import com.careerlens.entity.JobDescription;
import com.careerlens.repository.JobRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class JobService {

    private final JobRepository jobRepository;
    private final AiServiceClient aiServiceClient;
    private final ObjectMapper objectMapper;

    @Transactional
    public JobDescription createJobDescription(JobCreateRequest request) {
        log.info("Creating job description for title: {}", request.getTitle());

        String parsedJson = "";
        try {
            Map<String, Object> aiParsed = aiServiceClient.parseJobDescription(request.getTitle(), request.getDescription());
            parsedJson = objectMapper.writeValueAsString(aiParsed);
        } catch (Exception e) {
            log.warn("Could not parse job description via AI service: {}", e.getMessage());
        }

        JobDescription jd = JobDescription.builder()
                .title(request.getTitle() != null ? request.getTitle() : "Software Engineer")
                .company(request.getCompany() != null ? request.getCompany() : "Tech Company")
                .description(request.getDescription())
                .parsedJson(parsedJson)
                .build();

        return jobRepository.save(jd);
    }

    public List<JobDescription> getAllJobs() {
        return jobRepository.findAllByOrderByCreatedAtDesc();
    }

    public JobDescription getJobById(Long id) {
        return jobRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Job description not found with id: " + id));
    }
}
