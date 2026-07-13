package com.quizbank.quiz;

import java.sql.PreparedStatement;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.quizbank.question.Question;
import com.quizbank.question.QuestionRepository;

@Repository
public class QuizRepository {

	private final JdbcTemplate jdbcTemplate;
	private final QuestionRepository questionRepository;

	public QuizRepository(JdbcTemplate jdbcTemplate, QuestionRepository questionRepository) {
		this.jdbcTemplate = jdbcTemplate;
		this.questionRepository = questionRepository;
	}

	public List<Quiz> findAllSummaries() {
		return jdbcTemplate.query(
				"""
				SELECT q.id, q.name, q.created_at,
				       (SELECT COUNT(*) FROM quiz_questions qq WHERE qq.quiz_id = q.id) AS question_count
				FROM quizzes q
				ORDER BY q.id ASC
				""",
				(rs, rowNum) -> new Quiz(
						rs.getLong("id"),
						rs.getString("name"),
						null,
						null,
						rs.getInt("question_count"),
						rs.getObject("created_at", java.time.OffsetDateTime.class)));
	}

	public Optional<Quiz> findById(long id) {
		List<Quiz> headers = jdbcTemplate.query(
				"""
				SELECT id, name, created_at
				FROM quizzes
				WHERE id = ?
				""",
				(rs, rowNum) -> new Quiz(
						rs.getLong("id"),
						rs.getString("name"),
						null,
						null,
						null,
						rs.getObject("created_at", java.time.OffsetDateTime.class)),
				id);
		if (headers.isEmpty()) {
			return Optional.empty();
		}
		Quiz header = headers.get(0);
		List<Long> questionIds = jdbcTemplate.query(
				"""
				SELECT question_id
				FROM quiz_questions
				WHERE quiz_id = ?
				ORDER BY position ASC
				""",
				(rs, rowNum) -> rs.getLong("question_id"),
				id);
		List<Question> questions = new ArrayList<>();
		for (Long questionId : questionIds) {
			questionRepository.findById(questionId).ifPresent(questions::add);
		}
		return Optional.of(new Quiz(
				header.id(),
				header.name(),
				questionIds,
				questions,
				questionIds.size(),
				header.createdAt()));
	}

	@Transactional
	public Quiz insert(String name, List<Long> questionIds) {
		QuizValidator.validate(name, questionIds);
		ensureQuestionsExist(questionIds);

		KeyHolder keyHolder = new GeneratedKeyHolder();
		jdbcTemplate.update(connection -> {
			PreparedStatement ps = connection.prepareStatement(
					"INSERT INTO quizzes (name) VALUES (?)",
					new String[] {"id"});
			ps.setString(1, name.trim());
			return ps;
		}, keyHolder);
		Number key = keyHolder.getKey();
		if (key == null) {
			Object idValue = keyHolder.getKeys() == null ? null : keyHolder.getKeys().get("id");
			if (idValue instanceof Number number) {
				key = number;
			}
		}
		if (key == null) {
			throw new IllegalStateException("Failed to obtain quiz id");
		}
		long quizId = key.longValue();
		replaceQuestions(quizId, questionIds);
		return findById(quizId).orElseThrow();
	}

	@Transactional
	public Optional<Quiz> update(long id, String name, List<Long> questionIds) {
		if (findById(id).isEmpty()) {
			return Optional.empty();
		}
		QuizValidator.validate(name, questionIds);
		ensureQuestionsExist(questionIds);
		jdbcTemplate.update("UPDATE quizzes SET name = ? WHERE id = ?", name.trim(), id);
		jdbcTemplate.update("DELETE FROM quiz_questions WHERE quiz_id = ?", id);
		replaceQuestions(id, questionIds);
		return findById(id);
	}

	public boolean deleteById(long id) {
		int updated = jdbcTemplate.update("DELETE FROM quizzes WHERE id = ?", id);
		return updated > 0;
	}

	private void replaceQuestions(long quizId, List<Long> questionIds) {
		for (int i = 0; i < questionIds.size(); i++) {
			jdbcTemplate.update(
					"""
					INSERT INTO quiz_questions (quiz_id, question_id, position)
					VALUES (?, ?, ?)
					""",
					quizId,
					questionIds.get(i),
					i);
		}
	}

	private void ensureQuestionsExist(List<Long> questionIds) {
		for (Long questionId : questionIds) {
			if (questionRepository.findById(questionId).isEmpty()) {
				throw new QuizValidationException(List.of("Question not found: " + questionId));
			}
		}
	}
}
