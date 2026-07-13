package com.quizbank.web;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class QuestionApiTest {

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
	void createListSearchUpdateDelete() throws Exception {
		String createBody = """
				{
				  "question": "Largest continent?",
				  "option_a": "Asia",
				  "option_b": "Africa",
				  "option_c": "Europe",
				  "option_d": "Oceania",
				  "correct": "A",
				  "difficulty": "Easy"
				}
				""";

		String created = mockMvc.perform(post("/api/questions")
						.contentType(MediaType.APPLICATION_JSON)
						.content(createBody))
				.andExpect(status().isCreated())
				.andExpect(jsonPath("$.id").isNumber())
				.andExpect(jsonPath("$.option_a").value("Asia"))
				.andExpect(jsonPath("$.difficulty").value("Easy"))
				.andReturn()
				.getResponse()
				.getContentAsString();

		long id = Long.parseLong(created.replaceAll("(?s).*\"id\"\\s*:\\s*(\\d+).*", "$1"));

		mockMvc.perform(get("/api/questions"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$", hasSize(1)));

		mockMvc.perform(get("/api/questions").param("q", "continent"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$", hasSize(1)));

		mockMvc.perform(get("/api/questions").param("q", "nomatch"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$", hasSize(0)));

		String updateBody = """
				{
				  "question": "Largest continent on Earth?",
				  "option_a": "Asia",
				  "option_b": "Africa",
				  "option_c": "Europe",
				  "option_d": "Oceania",
				  "correct": "A",
				  "difficulty": "Medium"
				}
				""";

		mockMvc.perform(put("/api/questions/" + id)
						.contentType(MediaType.APPLICATION_JSON)
						.content(updateBody))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.question").value("Largest continent on Earth?"))
				.andExpect(jsonPath("$.difficulty").value("Medium"));

		mockMvc.perform(delete("/api/questions/" + id))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.deleted").value(true));

		mockMvc.perform(get("/api/questions/" + id))
				.andExpect(status().isNotFound())
				.andExpect(jsonPath("$.error").exists());
	}

	@Test
	void validationErrorReturns400() throws Exception {
		String badBody = """
				{
				  "question": "",
				  "option_a": "A",
				  "option_b": "B",
				  "option_c": "C",
				  "option_d": "D",
				  "correct": "A"
				}
				""";

		mockMvc.perform(post("/api/questions")
						.contentType(MediaType.APPLICATION_JSON)
						.content(badBody))
				.andExpect(status().isBadRequest())
				.andExpect(jsonPath("$.error").exists())
				.andExpect(jsonPath("$.errors").isArray());
	}

	@Test
	void omittedDifficultyDefaultsOnCreate() throws Exception {
		String body = """
				{
				  "question": "Default difficulty?",
				  "option_a": "A",
				  "option_b": "B",
				  "option_c": "C",
				  "option_d": "D",
				  "correct": "B"
				}
				""";

		mockMvc.perform(post("/api/questions")
						.contentType(MediaType.APPLICATION_JSON)
						.content(body))
				.andExpect(status().isCreated())
				.andExpect(jsonPath("$.difficulty").value("Medium"));
	}

	@Test
	void missingQuestionReturns404() throws Exception {
		mockMvc.perform(put("/api/questions/999999")
						.contentType(MediaType.APPLICATION_JSON)
						.content("""
								{
								  "question": "Nope",
								  "option_a": "A",
								  "option_b": "B",
								  "option_c": "C",
								  "option_d": "D",
								  "correct": "A",
								  "difficulty": "Easy"
								}
								"""))
				.andExpect(status().isNotFound());
	}
}
