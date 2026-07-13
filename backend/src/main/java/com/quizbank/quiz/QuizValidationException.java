package com.quizbank.quiz;

import java.util.List;

public class QuizValidationException extends RuntimeException {

	private final List<String> errors;

	public QuizValidationException(List<String> errors) {
		super(String.join("; ", errors));
		this.errors = List.copyOf(errors);
	}

	public List<String> getErrors() {
		return errors;
	}
}
