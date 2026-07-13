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

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class QuizApiTest {

	@Autowired
	private MockMvc mockMvc;

	@Autowired
	private JdbcTemplate jdbcTemplate;

	@BeforeEach
	void clean() {
		jdbcTemplate.update("DELETE FROM quiz_questions");
		jdbcTemplate.update("DELETE FROM quizzes");
		jdbcTemplate.update("DELETE FROM questions");
	}

	@Test
	void createRejectsFewerThanThreeQuestions() throws Exception {
		long q1 = createQuestion("Q1");
		long q2 = createQuestion("Q2");
		mockMvc.perform(post("/api/quizzes")
						.contentType(MediaType.APPLICATION_JSON)
						.content("""
								{"name":"Too small","question_ids":[%d,%d]}
								""".formatted(q1, q2)))
				.andExpect(status().isBadRequest())
				.andExpect(jsonPath("$.error").exists());
	}

	@Test
	void createListGetUpdateDelete() throws Exception {
		long q1 = createQuestion("Q1");
		long q2 = createQuestion("Q2");
		long q3 = createQuestion("Q3");
		long q4 = createQuestion("Q4");

		MvcResult created = mockMvc.perform(post("/api/quizzes")
						.contentType(MediaType.APPLICATION_JSON)
						.content("""
								{"name":"Geo Quiz","question_ids":[%d,%d,%d]}
								""".formatted(q1, q2, q3)))
				.andExpect(status().isCreated())
				.andExpect(jsonPath("$.name").value("Geo Quiz"))
				.andExpect(jsonPath("$.question_ids", hasSize(3)))
				.andExpect(jsonPath("$.questions", hasSize(3)))
				.andReturn();

		int quizId = JsonPath.read(created.getResponse().getContentAsString(), "$.id");

		mockMvc.perform(get("/api/quizzes"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$", hasSize(1)))
				.andExpect(jsonPath("$[0].question_count").value(3));

		mockMvc.perform(get("/api/quizzes/" + quizId))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.questions[0].question").value("Q1"));

		mockMvc.perform(put("/api/quizzes/" + quizId)
						.contentType(MediaType.APPLICATION_JSON)
						.content("""
								{"name":"Geo Quiz Updated","question_ids":[%d,%d,%d,%d]}
								""".formatted(q4, q3, q2, q1)))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.name").value("Geo Quiz Updated"))
				.andExpect(jsonPath("$.question_ids", hasSize(4)))
				.andExpect(jsonPath("$.questions[0].question").value("Q4"));

		mockMvc.perform(delete("/api/quizzes/" + quizId))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.deleted").value(true));

		mockMvc.perform(get("/api/quizzes/" + quizId))
				.andExpect(status().isNotFound());
	}

	@Test
	void createRejectsMissingQuestionId() throws Exception {
		long q1 = createQuestion("Q1");
		long q2 = createQuestion("Q2");
		mockMvc.perform(post("/api/quizzes")
						.contentType(MediaType.APPLICATION_JSON)
						.content("""
								{"name":"Bad refs","question_ids":[%d,%d,999999]}
								""".formatted(q1, q2)))
				.andExpect(status().isBadRequest());
	}

	private long createQuestion(String text) throws Exception {
		MvcResult result = mockMvc.perform(post("/api/questions")
						.contentType(MediaType.APPLICATION_JSON)
						.content("""
								{
								  "question": "%s",
								  "option_a": "A",
								  "option_b": "B",
								  "option_c": "C",
								  "option_d": "D",
								  "correct": "A",
								  "difficulty": "Easy"
								}
								""".formatted(text)))
				.andExpect(status().isCreated())
				.andReturn();
		return ((Number) JsonPath.read(result.getResponse().getContentAsString(), "$.id")).longValue();
	}
}
