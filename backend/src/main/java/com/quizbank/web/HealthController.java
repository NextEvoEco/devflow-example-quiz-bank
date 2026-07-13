package com.quizbank.web;

import java.util.Map;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

	private final JdbcTemplate jdbcTemplate;

	public HealthController(JdbcTemplate jdbcTemplate) {
		this.jdbcTemplate = jdbcTemplate;
	}

	@GetMapping("/api/health")
	public Map<String, Object> health() {
		Integer bootstrap = jdbcTemplate.queryForObject(
				"SELECT COUNT(*) FROM schema_bootstrap",
				Integer.class);
		return Map.of(
				"status", "ok",
				"app", "quiz-bank",
				"schemaBootstrapRows", bootstrap == null ? 0 : bootstrap);
	}
}
