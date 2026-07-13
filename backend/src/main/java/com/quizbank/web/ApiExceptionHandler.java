package com.quizbank.web;

import java.util.List;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import com.quizbank.question.QuestionValidationException;
import com.quizbank.quiz.QuizValidationException;

@RestControllerAdvice
public class ApiExceptionHandler {

	@ExceptionHandler(QuestionValidationException.class)
	public ResponseEntity<Map<String, Object>> handleValidation(QuestionValidationException ex) {
		return ResponseEntity.badRequest().body(Map.of(
				"error", ex.getMessage(),
				"errors", ex.getErrors()));
	}

	@ExceptionHandler(QuizValidationException.class)
	public ResponseEntity<Map<String, Object>> handleQuizValidation(QuizValidationException ex) {
		return ResponseEntity.badRequest().body(Map.of(
				"error", ex.getMessage(),
				"errors", ex.getErrors()));
	}

	@ExceptionHandler(NotFoundException.class)
	public ResponseEntity<Map<String, Object>> handleNotFound(NotFoundException ex) {
		return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of(
				"error", ex.getMessage()));
	}

	@ExceptionHandler(ConflictException.class)
	public ResponseEntity<Map<String, Object>> handleConflict(ConflictException ex) {
		return ResponseEntity.status(HttpStatus.CONFLICT).body(Map.of(
				"error", ex.getMessage()));
	}

	@ExceptionHandler(IllegalArgumentException.class)
	public ResponseEntity<Map<String, Object>> handleIllegalArgument(IllegalArgumentException ex) {
		return ResponseEntity.badRequest().body(Map.of("error", ex.getMessage()));
	}
}
