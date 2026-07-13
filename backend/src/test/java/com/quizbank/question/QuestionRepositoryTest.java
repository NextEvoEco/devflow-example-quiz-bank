package com.quizbank.question;

import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@SpringBootTest
class QuestionRepositoryTest {

	@Autowired
	private QuestionRepository repository;

	@Autowired
	private JdbcTemplate jdbcTemplate;

	@BeforeEach
	void cleanQuestions() {
		jdbcTemplate.update("DELETE FROM quiz_questions");
		jdbcTemplate.update("DELETE FROM quizzes");
		jdbcTemplate.update("DELETE FROM questions");
	}

	@Test
	void insertAndFindAll() {
		Question created = repository.insert(sample(null, "Capital of France?", "Medium"));
		assertThat(created.id()).isNotNull();
		assertThat(created.difficulty()).isEqualTo("Medium");

		List<Question> all = repository.findAll();
		assertThat(all).hasSize(1);
		assertThat(all.get(0).question()).isEqualTo("Capital of France?");
	}

	@Test
	void omittedDifficultyDefaultsToMedium() {
		Question created = repository.insert(sample(null, "Which ocean is the largest?", null));
		assertThat(created.difficulty()).isEqualTo(QuestionValidator.DEFAULT_DIFFICULTY);
	}

	@Test
	void searchFiltersByQuestionText() {
		repository.insert(sample(null, "Largest continent?", "Easy"));
		repository.insert(sample(null, "Longest river?", "Hard"));

		List<Question> matches = repository.search("continent");
		assertThat(matches).hasSize(1);
		assertThat(matches.get(0).question()).containsIgnoringCase("continent");
	}

	@Test
	void updateChangesFields() {
		Question created = repository.insert(sample(null, "Old text", "Easy"));
		Question updated = repository.update(
				created.id(),
				sample(null, "New text", "Hard")).orElseThrow();

		assertThat(updated.question()).isEqualTo("New text");
		assertThat(updated.difficulty()).isEqualTo("Hard");
	}

	@Test
	void deleteRemovesRow() {
		Question created = repository.insert(sample(null, "Delete me", "Easy"));
		assertThat(repository.deleteById(created.id())).isTrue();
		assertThat(repository.findById(created.id())).isEmpty();
	}

	@Test
	void invalidPayloadRejected() {
		assertThatThrownBy(() -> repository.insert(sample(null, " ", "Easy")))
				.isInstanceOf(QuestionValidationException.class)
				.hasMessageContaining("Question text is required");
	}

	@Test
	void invalidCorrectRejected() {
		Question bad = new Question(
				null, "Q?", "a", "b", "c", "d", "E", "Easy", null, null);
		assertThatThrownBy(() -> repository.insert(bad))
				.isInstanceOf(QuestionValidationException.class)
				.hasMessageContaining("Correct answer");
	}

	private static Question sample(Long id, String text, String difficulty) {
		return new Question(
				id,
				text,
				"Asia",
				"Africa",
				"Europe",
				"Oceania",
				"A",
				difficulty,
				null,
				null);
	}
}
