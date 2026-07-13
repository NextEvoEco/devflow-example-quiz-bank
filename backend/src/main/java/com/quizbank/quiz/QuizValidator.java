package com.quizbank.quiz;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public final class QuizValidator {

	public static final int MIN_QUESTIONS = 3;

	private QuizValidator() {
	}

	public static void validate(String name, List<Long> questionIds) {
		List<String> errors = new ArrayList<>();
		if (name == null || name.isBlank()) {
			errors.add("Quiz name is required");
		}
		if (questionIds == null || questionIds.size() < MIN_QUESTIONS) {
			errors.add("A quiz must include at least " + MIN_QUESTIONS + " questions");
		}
		if (questionIds != null) {
			Set<Long> seen = new HashSet<>();
			for (Long id : questionIds) {
				if (id == null) {
					errors.add("Question IDs must not be null");
					break;
				}
				if (!seen.add(id)) {
					errors.add("Duplicate question IDs are not allowed");
					break;
				}
			}
		}
		if (!errors.isEmpty()) {
			throw new QuizValidationException(errors);
		}
	}
}
