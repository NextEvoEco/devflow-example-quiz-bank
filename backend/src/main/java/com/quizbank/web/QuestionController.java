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
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.quizbank.question.Question;
import com.quizbank.question.QuestionRepository;

@RestController
@RequestMapping("/api/questions")
public class QuestionController {

	private final QuestionRepository questionRepository;

	public QuestionController(QuestionRepository questionRepository) {
		this.questionRepository = questionRepository;
	}

	@GetMapping
	public List<Question> list(@RequestParam(value = "q", required = false) String query) {
		if (query == null || query.isBlank()) {
			return questionRepository.findAll();
		}
		return questionRepository.search(query);
	}

	@GetMapping("/{id}")
	public Question get(@PathVariable long id) {
		return questionRepository.findById(id)
				.orElseThrow(() -> new NotFoundException("Question not found: " + id));
	}

	@PostMapping
	public ResponseEntity<Question> create(@RequestBody Question body) {
		Question created = questionRepository.insert(body);
		return ResponseEntity.status(HttpStatus.CREATED).body(created);
	}

	@PutMapping("/{id}")
	public Question update(@PathVariable long id, @RequestBody Question body) {
		return questionRepository.update(id, body)
				.orElseThrow(() -> new NotFoundException("Question not found: " + id));
	}

	@DeleteMapping("/{id}")
	public ResponseEntity<Map<String, Object>> delete(@PathVariable long id) {
		boolean deleted = questionRepository.deleteById(id);
		if (!deleted) {
			throw new NotFoundException("Question not found: " + id);
		}
		return ResponseEntity.ok(Map.of("deleted", true, "id", id));
	}
}
