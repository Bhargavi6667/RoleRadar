package com.careerlens.client;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Component
@Slf4j
public class AiServiceClient {

    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    public AiServiceClient(
            @Value("${ai.service.url:http://localhost:8000}") String aiServiceUrl,
            ObjectMapper objectMapper) {
        this.webClient = WebClient.builder()
                .baseUrl(aiServiceUrl)
                .build();
        this.objectMapper = objectMapper;
    }

    public Map<String, Object> checkHealth() {
        try {
            return webClient.get()
                    .uri("/health")
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.warn("AI service unreachable at /health: {}", e.getMessage());
            Map<String, Object> fallback = new HashMap<>();
            fallback.put("status", "offline");
            fallback.put("error", e.getMessage());
            return fallback;
        }
    }

    public Map<String, Object> parseResumeFile(MultipartFile file) {
        try {
            MultipartBodyBuilder builder = new MultipartBodyBuilder();
            ByteArrayResource resource = new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            };
            builder.part("file", resource, MediaType.APPLICATION_PDF);

            return webClient.post()
                    .uri("/ai/resume/parse")
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .body(BodyInserters.fromMultipartData(builder.build()))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.error("Failed to parse resume via AI service: {}", e.getMessage());
            throw new RuntimeException("AI service failed to parse PDF resume: " + e.getMessage(), e);
        }
    }

    public Map<String, Object> parseResumeText(String text) {
        try {
            MultipartBodyBuilder builder = new MultipartBodyBuilder();
            builder.part("text", text);

            return webClient.post()
                    .uri("/ai/resume/parse")
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .body(BodyInserters.fromMultipartData(builder.build()))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.error("Failed to parse resume text via AI service: {}", e.getMessage());
            throw new RuntimeException("AI service failed to parse resume text: " + e.getMessage(), e);
        }
    }

    public Map<String, Object> parseJobDescription(String title, String description) {
        try {
            Map<String, String> payload = new HashMap<>();
            payload.put("title", title);
            payload.put("description", description);

            return webClient.post()
                    .uri("/ai/analysis/parse-job")
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(payload)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.error("Failed to parse job description via AI service: {}", e.getMessage());
            throw new RuntimeException("AI service failed to parse job description: " + e.getMessage(), e);
        }
    }

    public Map<String, Object> analyzeMatch(String resumeText, String jobDescription) {
        try {
            Map<String, Object> payload = new HashMap<>();
            payload.put("resume_text", resumeText);
            payload.put("job_description", jobDescription);

            return webClient.post()
                    .uri("/ai/analysis/match")
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(payload)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.error("Failed to analyze match via AI service: {}", e.getMessage());
            throw new RuntimeException("AI service failed to analyze match: " + e.getMessage(), e);
        }
    }

    public Map<String, Object> analyzeRoleFit(String resumeText) {
        try {
            Map<String, Object> payload = new HashMap<>();
            payload.put("resume_text", resumeText);

            return webClient.post()
                    .uri("/ai/analysis/role-fit")
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(payload)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.error("Failed to analyze role fit via AI service: {}", e.getMessage());
            throw new RuntimeException("AI service failed to analyze role fit: " + e.getMessage(), e);
        }
    }

    /** Generic JSON POST to the AI service, used by the role-based interview endpoints. */
    public Map<String, Object> postJson(String uri, Map<String, Object> payload) {
        try {
            return webClient.post()
                    .uri(uri)
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(payload)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.error("AI service call {} failed: {}", uri, e.getMessage());
            throw new RuntimeException("AI service request failed: " + e.getMessage(), e);
        }
    }

    public Map<String, Object> startInterview(String resumeText, String jobDescription, List<String> topics) {
        try {
            Map<String, Object> payload = new HashMap<>();
            payload.put("resume_text", resumeText);
            payload.put("job_description", jobDescription);
            payload.put("topics", topics != null ? topics : List.of());

            return webClient.post()
                    .uri("/ai/interview/start")
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(payload)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.error("Failed to start interview via AI service: {}", e.getMessage());
            throw new RuntimeException("AI service failed to start interview: " + e.getMessage(), e);
        }
    }

    public Map<String, Object> submitInterviewAnswer(String question, String answer, String resumeContext, String jobContext) {
        try {
            Map<String, Object> payload = new HashMap<>();
            payload.put("question", question);
            payload.put("answer", answer);
            payload.put("resume_context", resumeContext);
            payload.put("job_context", jobContext);

            return webClient.post()
                    .uri("/ai/interview/respond")
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(payload)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();
        } catch (Exception e) {
            log.error("Failed to evaluate answer via AI service: {}", e.getMessage());
            throw new RuntimeException("AI service failed to evaluate answer: " + e.getMessage(), e);
        }
    }
}
