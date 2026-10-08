package com.careerlens.controller;

import com.careerlens.dto.AnalysisRequest;
import com.careerlens.dto.AnalysisResponse;
import com.careerlens.dto.RoleFitRequest;
import com.careerlens.entity.Analysis;
import com.careerlens.service.AnalysisService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/analyses")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class AnalysisController {

    private final AnalysisService analysisService;

    @PostMapping("/run")
    public ResponseEntity<AnalysisResponse> runAnalysis(@RequestBody AnalysisRequest request) {
        AnalysisResponse response = analysisService.analyze(request);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/role-fit")
    public ResponseEntity<Map<String, Object>> roleFit(@RequestBody RoleFitRequest request) {
        return ResponseEntity.ok(analysisService.roleFit(request));
    }

    @GetMapping
    public ResponseEntity<List<Analysis>> getAllAnalyses() {
        return ResponseEntity.ok(analysisService.getAllAnalyses());
    }

    @GetMapping("/{id}")
    public ResponseEntity<AnalysisResponse> getAnalysisById(@PathVariable Long id) {
        return ResponseEntity.ok(analysisService.getAnalysisById(id));
    }
}
