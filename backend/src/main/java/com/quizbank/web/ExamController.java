package com.quizbank.web;

import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.quizbank.exam.ExamAttemptRepository;

@RestController
@RequestMapping("/api/exams")
public class ExamController {

	private final ExamAttemptRepository attempts;

	public ExamController(ExamAttemptRepository attempts) {
		this.attempts = attempts;
	}

	@PostMapping("/attempts")
	public ResponseEntity<Map<String, Long>> createAttempt(@RequestBody CreateAttemptRequest body) {
		if (!attempts.quizExists(body.quizId())) {
			throw new NotFoundException("Quiz not found: " + body.quizId());
		}
		return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("attempt_id", attempts.createAttempt(body.quizId())));
	}

	@PutMapping("/attempts/{attemptId}/answers/{questionId}")
	public ResponseEntity<Void> saveAnswer(@PathVariable long attemptId, @PathVariable long questionId,
			@RequestBody AnswerRequest body) {
		ExamAttemptRepository.Attempt attempt = attempts.findAttempt(attemptId)
				.orElseThrow(() -> new NotFoundException("Attempt not found: " + attemptId));
		if (attempt.submittedAt() != null) {
			throw new ConflictException("Attempt has already been submitted");
		}
		if (!attempts.questionBelongsToQuiz(attempt.quizId(), questionId)) {
			throw new NotFoundException("Question not found in this quiz: " + questionId);
		}
		String option = body.selectedOption();
		if (option != null && !option.matches("[ABCD]")) {
			throw new IllegalArgumentException("selected_option must be A, B, C, D, or null");
		}
		attempts.saveAnswer(attemptId, questionId, option);
		return ResponseEntity.noContent().build();
	}

	@PostMapping("/attempts/{attemptId}/submit")
	public ExamAttemptRepository.Result submit(@PathVariable long attemptId) {
		ExamAttemptRepository.Attempt attempt = attempts.findAttempt(attemptId)
				.orElseThrow(() -> new NotFoundException("Attempt not found: " + attemptId));
		if (attempt.submittedAt() != null) {
			throw new ConflictException("Attempt has already been submitted");
		}
		return attempts.submit(attemptId);
	}

	public record CreateAttemptRequest(@JsonProperty("quiz_id") long quizId) {}
	public record AnswerRequest(@JsonProperty("selected_option") String selectedOption) {}
}
