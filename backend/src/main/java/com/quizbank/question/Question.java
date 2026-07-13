package com.quizbank.question;

import java.time.OffsetDateTime;

import com.fasterxml.jackson.annotation.JsonProperty;

public record Question(
		Long id,
		String question,
		@JsonProperty("option_a") String optionA,
		@JsonProperty("option_b") String optionB,
		@JsonProperty("option_c") String optionC,
		@JsonProperty("option_d") String optionD,
		String correct,
		String difficulty,
		@JsonProperty("created_at") OffsetDateTime createdAt,
		@JsonProperty("updated_at") OffsetDateTime updatedAt
) {
	public Question withDefaults() {
		String resolvedDifficulty = (difficulty == null || difficulty.isBlank())
				? QuestionValidator.DEFAULT_DIFFICULTY
				: difficulty.trim();
		return new Question(
				id,
				question == null ? null : question.trim(),
				optionA == null ? null : optionA.trim(),
				optionB == null ? null : optionB.trim(),
				optionC == null ? null : optionC.trim(),
				optionD == null ? null : optionD.trim(),
				correct == null ? null : correct.trim().toUpperCase(),
				resolvedDifficulty,
				createdAt,
				updatedAt
		);
	}
}
