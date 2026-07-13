package com.quizbank.question;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class QuestionValidatorTest {

	@Test
	void appliesDefaultDifficultyWhenOmitted() {
		Question prepared = QuestionValidator.prepare(new Question(
				null, "Q", "a", "b", "c", "d", "A", null, null, null));
		assertThat(prepared.difficulty()).isEqualTo("Medium");
	}

	@Test
	void rejectsMissingOptions() {
		assertThatThrownBy(() -> QuestionValidator.prepare(new Question(
				null, "Q", "a", "", "c", "d", "A", "Easy", null, null)))
				.isInstanceOf(QuestionValidationException.class)
				.hasMessageContaining("Option B is required");
	}
}
