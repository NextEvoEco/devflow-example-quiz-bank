package com.quizbank.question;

import java.util.List;

public class QuestionValidationException extends RuntimeException {

	private final List<String> errors;

	public QuestionValidationException(List<String> errors) {
		super(String.join("; ", errors));
		this.errors = List.copyOf(errors);
	}

	public List<String> getErrors() {
		return errors;
	}
}
