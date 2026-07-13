package com.quizbank.web;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import com.jayway.jsonpath.JsonPath;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class ExamApiTest {
	@Autowired private MockMvc mockMvc;
	@Autowired private JdbcTemplate jdbcTemplate;

	@BeforeEach
	void clean() {
		jdbcTemplate.update("DELETE FROM exam_answers");
		jdbcTemplate.update("DELETE FROM exam_attempts");
		jdbcTemplate.update("DELETE FROM quiz_questions");
		jdbcTemplate.update("DELETE FROM quizzes");
		jdbcTemplate.update("DELETE FROM questions");
	}

	@Test
	void examFlowScoresAndRejectsDoubleSubmit() throws Exception {
		long q1 = createQuestion("Correct");
		long q2 = createQuestion("Wrong");
		long q3 = createQuestion("Unanswered");
		long quizId = createQuiz(q1, q2, q3);

		MvcResult attemptResult = mockMvc.perform(post("/api/exams/attempts")
						.contentType(MediaType.APPLICATION_JSON).content("{\"quiz_id\":" + quizId + "}"))
				.andExpect(status().isCreated()).andReturn();
		long attemptId = ((Number) JsonPath.read(attemptResult.getResponse().getContentAsString(), "$.attempt_id")).longValue();

		mockMvc.perform(put("/api/exams/attempts/" + attemptId + "/answers/" + q1)
						.contentType(MediaType.APPLICATION_JSON).content("{\"selected_option\":\"A\"}"))
				.andExpect(status().isNoContent());
		mockMvc.perform(put("/api/exams/attempts/" + attemptId + "/answers/" + q2)
						.contentType(MediaType.APPLICATION_JSON).content("{\"selected_option\":\"B\"}"))
				.andExpect(status().isNoContent());

		mockMvc.perform(post("/api/exams/attempts/" + attemptId + "/submit"))
				.andExpect(status().isOk()).andExpect(jsonPath("$.score").value(1))
				.andExpect(jsonPath("$.total").value(3)).andExpect(jsonPath("$.percentage").value(33))
				.andExpect(jsonPath("$.answers[0].question_text").value("Correct"));
		mockMvc.perform(post("/api/exams/attempts/" + attemptId + "/submit"))
				.andExpect(status().isConflict());
	}

	@Test
	void missingQuizAndAttemptReturnNotFound() throws Exception {
		mockMvc.perform(post("/api/exams/attempts").contentType(MediaType.APPLICATION_JSON)
						.content("{\"quiz_id\":999999}")).andExpect(status().isNotFound());
		mockMvc.perform(post("/api/exams/attempts/999999/submit")).andExpect(status().isNotFound());
	}

	private long createQuestion(String text) {
		return jdbcTemplate.queryForObject("""
				INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct, difficulty)
				VALUES (?, 'A', 'B', 'C', 'D', 'A', 'Easy') RETURNING id
				""", Long.class, text);
	}

	private long createQuiz(long q1, long q2, long q3) {
		long quizId = jdbcTemplate.queryForObject("INSERT INTO quizzes (name) VALUES ('Exam Quiz') RETURNING id", Long.class);
		jdbcTemplate.update("INSERT INTO quiz_questions (quiz_id, question_id, position) VALUES (?, ?, 0)", quizId, q1);
		jdbcTemplate.update("INSERT INTO quiz_questions (quiz_id, question_id, position) VALUES (?, ?, 1)", quizId, q2);
		jdbcTemplate.update("INSERT INTO quiz_questions (quiz_id, question_id, position) VALUES (?, ?, 2)", quizId, q3);
		return quizId;
	}
}
