package com.careerlens.repository;

import com.careerlens.entity.Analysis;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface AnalysisRepository extends JpaRepository<Analysis, Long> {
    List<Analysis> findByResumeIdOrderByCreatedAtDesc(Long resumeId);
    List<Analysis> findAllByOrderByCreatedAtDesc();
    Optional<Analysis> findFirstByResumeIdAndJobDescriptionIdOrderByCreatedAtDesc(Long resumeId, Long jobDescriptionId);
}
