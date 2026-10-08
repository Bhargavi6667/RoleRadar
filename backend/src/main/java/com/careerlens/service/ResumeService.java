package com.careerlens.service;

import com.careerlens.client.AiServiceClient;
import com.careerlens.dto.ResumeUploadResponse;
import com.careerlens.entity.Resume;
import com.careerlens.repository.ResumeRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class ResumeService {

    private final ResumeRepository resumeRepository;
    private final AiServiceClient aiServiceClient;
    private final ObjectMapper objectMapper;

    @Transactional
    public ResumeUploadResponse uploadResume(MultipartFile file) {
        log.info("Processing resume upload: {}", file.getOriginalFilename());
        Map<String, Object> aiResponse = aiServiceClient.parseResumeFile(file);

        return saveParsedResume(file.getOriginalFilename(), aiResponse);
    }

    @Transactional
    public ResumeUploadResponse uploadResumeText(String text, String fileName) {
        log.info("Processing resume raw text upload");
        Map<String, Object> aiResponse = aiServiceClient.parseResumeText(text);

        return saveParsedResume(fileName != null ? fileName : "manual-resume.txt", aiResponse);
    }

    private ResumeUploadResponse saveParsedResume(String fileName, Map<String, Object> aiResponse) {
        Map<String, Object> resumeData = (Map<String, Object>) aiResponse.get("resume");
        String extractedText = resumeData != null && resumeData.get("raw_text") != null 
                ? resumeData.get("raw_text").toString() : "";
        String candidateName = resumeData != null && resumeData.get("name") != null 
                ? resumeData.get("name").toString() : "Candidate";
        String candidateEmail = resumeData != null && resumeData.get("email") != null 
                ? resumeData.get("email").toString() : "";

        String jsonStr = "";
        try {
            jsonStr = objectMapper.writeValueAsString(resumeData);
        } catch (Exception e) {
            log.warn("Could not serialize parsed resume to JSON: {}", e.getMessage());
        }

        Resume resume = Resume.builder()
                .fileName(fileName)
                .candidateName(candidateName)
                .candidateEmail(candidateEmail)
                .extractedText(extractedText)
                .parsedJson(jsonStr)
                .build();

        Resume saved = resumeRepository.save(resume);

        return ResumeUploadResponse.builder()
                .id(saved.getId())
                .fileName(saved.getFileName())
                .candidateName(saved.getCandidateName())
                .candidateEmail(saved.getCandidateEmail())
                .extractedText(saved.getExtractedText())
                .parsedDetails(resumeData)
                .build();
    }

    public List<Resume> getAllResumes() {
        return resumeRepository.findAllByOrderByCreatedAtDesc();
    }

    public Resume getResumeById(Long id) {
        return resumeRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Resume not found with id: " + id));
    }
}
