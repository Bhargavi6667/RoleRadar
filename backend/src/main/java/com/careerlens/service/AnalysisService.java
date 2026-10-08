package com.careerlens.service;

import com.careerlens.client.AiServiceClient;
import com.careerlens.dto.AnalysisRequest;
import com.careerlens.dto.AnalysisResponse;
import com.careerlens.dto.RoleFitRequest;
import com.careerlens.entity.Analysis;
import com.careerlens.entity.JobDescription;
import com.careerlens.entity.Resume;
import com.careerlens.repository.AnalysisRepository;
import com.careerlens.repository.JobRepository;
import com.careerlens.repository.ResumeRepository;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class AnalysisService {

    private final AnalysisRepository analysisRepository;
    private final ResumeRepository resumeRepository;
    private final JobRepository jobRepository;
    private final AiServiceClient aiServiceClient;
    private final ObjectMapper objectMapper;
    private final VacancyService vacancyService;

    @Transactional
    public AnalysisResponse analyze(AnalysisRequest request) {
        Resume resume = null;
        JobDescription job = null;
        String resumeText = request.getResumeText();
        String jobText = request.getJobDescription();

        if (request.getResumeId() != null) {
            resume = resumeRepository.findById(request.getResumeId())
                    .orElseThrow(() -> new RuntimeException("Resume not found with id: " + request.getResumeId()));
            if (resumeText == null || resumeText.isBlank()) {
                resumeText = resume.getExtractedText();
            }
        }

        if (request.getJobDescriptionId() != null) {
            job = jobRepository.findById(request.getJobDescriptionId())
                    .orElseThrow(() -> new RuntimeException("Job not found with id: " + request.getJobDescriptionId()));
            if (jobText == null || jobText.isBlank()) {
                jobText = job.getDescription();
            }
        }

        log.info("Requesting match analysis from AI microservice");
        Map<String, Object> aiResult = aiServiceClient.analyzeMatch(resumeText, jobText);

        Double overallScore = 0.0;
        if (aiResult.get("overall_score") instanceof Number num) {
            overallScore = num.doubleValue();
        }

        String reportJson = "";
        try {
            reportJson = objectMapper.writeValueAsString(aiResult);
        } catch (Exception e) {
            log.warn("Could not serialize analysis report: {}", e.getMessage());
        }

        Analysis saved = null;
        if (resume != null && job != null) {
            Analysis analysis = Analysis.builder()
                    .resume(resume)
                    .jobDescription(job)
                    .overallScore(overallScore)
                    .report(reportJson)
                    .build();
            saved = analysisRepository.save(analysis);
        }

        return mapToAnalysisResponse(saved != null ? saved.getId() : null,
                request.getResumeId(),
                request.getJobDescriptionId(),
                overallScore,
                aiResult);
    }

    /**
     * Resume-only analysis: which roles does this resume suit, how well, what to improve,
     * and which companies hire for those roles. No job description required.
     */
    @SuppressWarnings("unchecked")
    public Map<String, Object> roleFit(RoleFitRequest request) {
        String resumeText = request.getResumeText();

        if ((resumeText == null || resumeText.isBlank()) && request.getResumeId() != null) {
            Resume resume = resumeRepository.findById(request.getResumeId())
                    .orElseThrow(() -> new RuntimeException("Resume not found with id: " + request.getResumeId()));
            resumeText = resume.getExtractedText();
        }
        if (resumeText == null || resumeText.isBlank()) {
            throw new IllegalArgumentException("Resume text is empty. Upload a text-based PDF resume.");
        }

        log.info("Requesting role-fit analysis from AI microservice");
        Map<String, Object> result = new HashMap<>(aiServiceClient.analyzeRoleFit(resumeText));

        // Attach vacancies for the top 3 matching roles, keyed by role id
        Map<String, Object> vacancies = new LinkedHashMap<>();
        Object scores = result.get("role_scores");
        if (scores instanceof List<?> list) {
            for (Object o : list.stream().limit(3).toList()) {
                if (o instanceof Map<?, ?> row && row.get("role_id") != null) {
                    String roleId = row.get("role_id").toString();
                    vacancies.put(roleId, vacancyService.getForRole(roleId));
                }
            }
        }
        result.put("vacancies", vacancies);
        result.put("resume_id", request.getResumeId());
        return result;
    }

    public List<Analysis> getAllAnalyses() {
        return analysisRepository.findAllByOrderByCreatedAtDesc();
    }

    public AnalysisResponse getAnalysisById(Long id) {
        Analysis analysis = analysisRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Analysis not found with id: " + id));

        Map<String, Object> reportData = Map.of();
        try {
            if (analysis.getReport() != null && !analysis.getReport().isBlank()) {
                reportData = objectMapper.readValue(analysis.getReport(), new TypeReference<Map<String, Object>>() {});
            }
        } catch (Exception e) {
            log.error("Failed to parse stored report JSON: {}", e.getMessage());
        }

        return mapToAnalysisResponse(
                analysis.getId(),
                analysis.getResume().getId(),
                analysis.getJobDescription().getId(),
                analysis.getOverallScore(),
                reportData
        );
    }

    private AnalysisResponse mapToAnalysisResponse(
            Long id,
            Long resumeId,
            Long jobId,
            Double overallScore,
            Map<String, Object> aiResult) {

        Map<String, Object> breakdown = (Map<String, Object>) aiResult.get("scoring_breakdown");
        List<String> strengths = (List<String>) aiResult.get("strengths");
        List<String> skillGaps = (List<String>) aiResult.get("skill_gaps");
        List<Map<String, Object>> evidence = (List<Map<String, Object>>) aiResult.get("evidence");
        List<String> recommendations = (List<String>) aiResult.get("recommendations");
        List<String> interviewTopics = (List<String>) aiResult.get("interview_topics");
        List<Map<String, Object>> roadmap = (List<Map<String, Object>>) aiResult.get("learning_roadmap");

        return AnalysisResponse.builder()
                .id(id)
                .resumeId(resumeId)
                .jobDescriptionId(jobId)
                .overallScore(overallScore)
                .scoringBreakdown(breakdown)
                .strengths(strengths)
                .skillGaps(skillGaps)
                .evidence(evidence)
                .recommendations(recommendations)
                .interviewTopics(interviewTopics)
                .learningRoadmap(roadmap)
                .build();
    }
}
