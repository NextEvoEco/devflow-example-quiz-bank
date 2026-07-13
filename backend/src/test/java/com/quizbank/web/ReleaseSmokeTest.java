package com.quizbank.web;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class ReleaseSmokeTest {

	@Autowired
	private MockMvc mockMvc;

	@Test
	void healthAndSpaIndexAreReachableThroughMvc() throws Exception {
		mockMvc.perform(get("/api/health"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.status").value("ok"));

		mockMvc.perform(get("/"))
				.andExpect(status().isOk());
	}

	@Test
	void questionCrudBaselineWorks() throws Exception {
		String body = """
				{
				  "question": "Release smoke question?",
				  "option_a": "A1",
				  "option_b": "B1",
				  "option_c": "C1",
				  "option_d": "D1",
				  "correct": "A",
				  "difficulty": "Easy"
				}
				""";

		mockMvc.perform(post("/api/questions")
						.contentType(MediaType.APPLICATION_JSON)
						.content(body))
				.andExpect(status().isCreated())
				.andExpect(jsonPath("$.id").isNumber());

		mockMvc.perform(get("/api/questions").param("q", "Release smoke"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$[0].question").value("Release smoke question?"));
	}
}
