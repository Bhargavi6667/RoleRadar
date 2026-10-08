package com.careerlens.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AnalysisRequest {
    private Long resumeId;
    private Long jobDescriptionId;
    private String resumeText;
    private String jobDescription;
}
