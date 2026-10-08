package com.careerlens.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ResumeUploadResponse {
    private Long id;
    private String fileName;
    private String candidateName;
    private String candidateEmail;
    private String extractedText;
    private Object parsedDetails;
}
