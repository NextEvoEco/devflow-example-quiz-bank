package com.quizbank.question;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public final class QuestionValidator {

	public static final String DEFAULT_DIFFICULTY = "Medium";
	private static final Set<String> VALID_CORRECT = Set.of("A", "B", "C", "D");
	private static final Set<String> VALID_DIFFICULTY = Set.of("Easy", "Medium", "Hard");

	private QuestionValidator() {
	}

	public static Question prepare(Question input) {
		if (input == null) {
			throw new QuestionValidationException(List.of("Question payload is required"));
		}
		Question normalized = input.withDefaults();
		List<String> errors = new ArrayList<>();

		if (isBlank(normalized.question())) {
			errors.add("Question text is required");
		}
		if (isBlank(normalized.optionA())) {
			errors.add("Option A is required");
		}
		if (isBlank(normalized.optionB())) {
			errors.add("Option B is required");
		}
		if (isBlank(normalized.optionC())) {
			errors.add("Option C is required");
		}
		if (isBlank(normalized.optionD())) {
			errors.add("Option D is required");
		}
		if (isBlank(normalized.correct()) || !VALID_CORRECT.contains(normalized.correct())) {
			errors.add("Correct answer must be one of A, B, C, D");
		}
		if (!VALID_DIFFICULTY.contains(normalized.difficulty())) {
			errors.add("Difficulty must be one of Easy, Medium, Hard");
		}

		if (!errors.isEmpty()) {
			throw new QuestionValidationException(errors);
		}
		return normalized;
	}

	private static boolean isBlank(String value) {
		return value == null || value.isBlank();
	}
}
