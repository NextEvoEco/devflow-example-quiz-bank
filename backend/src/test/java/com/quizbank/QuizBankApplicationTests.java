package com.quizbank;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class QuizBankApplicationTests {

	@Autowired
	private JdbcTemplate jdbcTemplate;

	@Test
	void contextLoads() {
	}

	@Test
	void flywayBaselineApplied() {
		Integer count = jdbcTemplate.queryForObject(
				"SELECT COUNT(*) FROM schema_bootstrap",
				Integer.class);
		assertThat(count).isEqualTo(1);
	}
}
