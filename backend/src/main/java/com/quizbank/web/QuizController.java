package com.quizbank.web;

import java.util.List;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.quizbank.quiz.Quiz;
import com.quizbank.quiz.QuizRepository;

@RestController
@RequestMapping("/api/quizzes")
public class QuizController {

	private final QuizRepository quizRepository;

	public QuizController(QuizRepository quizRepository) {
		this.quizRepository = quizRepository;
	}

	@GetMapping
	public List<Quiz> list() {
		return quizRepository.findAllSummaries();
	}

	@GetMapping("/{id}")
	public Quiz get(@PathVariable long id) {
		return quizRepository.findById(id)
				.orElseThrow(() -> new NotFoundException("Quiz not found: " + id));
	}

	@PostMapping
	public ResponseEntity<Quiz> create(@RequestBody QuizRequest body) {
		Quiz created = quizRepository.insert(body.name(), body.questionIds());
		return ResponseEntity.status(HttpStatus.CREATED).body(created);
	}

	@PutMapping("/{id}")
	public Quiz update(@PathVariable long id, @RequestBody QuizRequest body) {
		return quizRepository.update(id, body.name(), body.questionIds())
				.orElseThrow(() -> new NotFoundException("Quiz not found: " + id));
	}

	@DeleteMapping("/{id}")
	public ResponseEntity<Map<String, Object>> delete(@PathVariable long id) {
		if (!quizRepository.deleteById(id)) {
			throw new NotFoundException("Quiz not found: " + id);
		}
		return ResponseEntity.ok(Map.of("deleted", true, "id", id));
	}

	public record QuizRequest(
			String name,
			@JsonProperty("question_ids") List<Long> questionIds
	) {
	}
}
