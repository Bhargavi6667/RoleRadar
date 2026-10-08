package com.careerlens.controller;

import com.careerlens.dto.ResumeUploadResponse;
import com.careerlens.entity.Resume;
import com.careerlens.service.ResumeService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/resumes")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class ResumeController {

    private final ResumeService resumeService;

    @PostMapping("/upload")
    public ResponseEntity<ResumeUploadResponse> uploadResume(
            @RequestParam("file") MultipartFile file) {
        ResumeUploadResponse response = resumeService.uploadResume(file);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/text")
    public ResponseEntity<ResumeUploadResponse> uploadResumeText(
            @RequestBody Map<String, String> payload) {
        String text = payload.get("text");
        String fileName = payload.getOrDefault("fileName", "resume.txt");
        ResumeUploadResponse response = resumeService.uploadResumeText(text, fileName);
        return ResponseEntity.ok(response);
    }

    @GetMapping
    public ResponseEntity<List<Resume>> getAllResumes() {
        return ResponseEntity.ok(resumeService.getAllResumes());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Resume> getResumeById(@PathVariable Long id) {
        return ResponseEntity.ok(resumeService.getResumeById(id));
    }
}
