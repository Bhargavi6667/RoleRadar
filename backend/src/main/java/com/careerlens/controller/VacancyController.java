package com.careerlens.controller;

import com.careerlens.service.VacancyService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/vacancies")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class VacancyController {

    private final VacancyService vacancyService;

    @GetMapping("/{roleId}")
    public ResponseEntity<List<Map<String, Object>>> getByRole(@PathVariable String roleId) {
        return ResponseEntity.ok(vacancyService.getForRole(roleId));
    }
}
