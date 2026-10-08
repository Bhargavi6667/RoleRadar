package com.careerlens.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AnalysisResponse {
    private Long id;
    private Long resumeId;
    private Long jobDescriptionId;
    private Double overallScore;
    private Map<String, Object> scoringBreakdown;
    private List<String> strengths;
    private List<String> skillGaps;
    private List<Map<String, Object>> evidence;
    private List<String> recommendations;
    private List<String> interviewTopics;
    private List<Map<String, Object>> learningRoadmap;
}
