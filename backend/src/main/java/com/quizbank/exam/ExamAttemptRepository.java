package com.quizbank.exam;

import java.sql.PreparedStatement;
import java.util.List;
import java.util.Optional;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.fasterxml.jackson.annotation.JsonProperty;

@Repository
public class ExamAttemptRepository {

	private final JdbcTemplate jdbcTemplate;

	public ExamAttemptRepository(JdbcTemplate jdbcTemplate) {
		this.jdbcTemplate = jdbcTemplate;
	}

	public boolean quizExists(long quizId) {
		return Boolean.TRUE.equals(jdbcTemplate.queryForObject(
				"SELECT EXISTS(SELECT 1 FROM quizzes WHERE id = ?)", Boolean.class, quizId));
	}

	@Transactional
	public long createAttempt(long quizId) {
		KeyHolder keyHolder = new GeneratedKeyHolder();
		jdbcTemplate.update(connection -> {
			PreparedStatement statement = connection.prepareStatement(
					"INSERT INTO exam_attempts (quiz_id) VALUES (?)", new String[] {"id"});
			statement.setLong(1, quizId);
			return statement;
		}, keyHolder);
		Number key = keyHolder.getKey();
		if (key == null) {
			throw new IllegalStateException("Failed to obtain attempt id");
		}
		return key.longValue();
	}

	public Optional<Attempt> findAttempt(long attemptId) {
		List<Attempt> attempts = jdbcTemplate.query(
				"SELECT id, quiz_id, score, total, submitted_at FROM exam_attempts WHERE id = ?",
				(rs, rowNum) -> new Attempt(
						rs.getLong("id"),
						rs.getLong("quiz_id"),
						(Integer) rs.getObject("score"),
						(Integer) rs.getObject("total"),
						rs.getObject("submitted_at", java.time.OffsetDateTime.class)),
				attemptId);
		return attempts.stream().findFirst();
	}

	public boolean questionBelongsToQuiz(long quizId, long questionId) {
		return Boolean.TRUE.equals(jdbcTemplate.queryForObject(
				"SELECT EXISTS(SELECT 1 FROM quiz_questions WHERE quiz_id = ? AND question_id = ?)",
				Boolean.class, quizId, questionId));
	}

	public void saveAnswer(long attemptId, long questionId, String selectedOption) {
		jdbcTemplate.update(
				"""
				INSERT INTO exam_answers (attempt_id, question_id, selected_option)
				VALUES (?, ?, ?)
				ON CONFLICT (attempt_id, question_id)
				DO UPDATE SET selected_option = EXCLUDED.selected_option
				""",
				attemptId, questionId, selectedOption);
	}

	@Transactional
	public Result submit(long attemptId) {
		Attempt attempt = findAttempt(attemptId).orElseThrow();
		int total = jdbcTemplate.queryForObject(
				"SELECT COUNT(*) FROM quiz_questions WHERE quiz_id = ?", Integer.class, attempt.quizId());
		int score = jdbcTemplate.queryForObject(
				"""
				SELECT COUNT(*)
				FROM quiz_questions qq
				LEFT JOIN exam_answers ea ON ea.attempt_id = ? AND ea.question_id = qq.question_id
				JOIN questions q ON q.id = qq.question_id
				WHERE qq.quiz_id = ? AND ea.selected_option = q.correct
				""",
				Integer.class, attemptId, attempt.quizId());
		jdbcTemplate.update(
				"UPDATE exam_attempts SET score = ?, total = ?, submitted_at = NOW() WHERE id = ?",
				score, total, attemptId);

		List<AnswerResult> answers = jdbcTemplate.query(
				"""
				SELECT qq.question_id, q.question, ea.selected_option, q.correct,
				       q.option_a, q.option_b, q.option_c, q.option_d
				FROM quiz_questions qq
				JOIN questions q ON q.id = qq.question_id
				LEFT JOIN exam_answers ea ON ea.attempt_id = ? AND ea.question_id = qq.question_id
				WHERE qq.quiz_id = ?
				ORDER BY qq.position
				""",
				(rs, rowNum) -> {
					String selected = rs.getString("selected_option");
					String correct = rs.getString("correct");
					return new AnswerResult(
							rs.getLong("question_id"), rs.getString("question"), selected, correct,
							selected != null && selected.equals(correct),
							rs.getString("option_a"), rs.getString("option_b"),
							rs.getString("option_c"), rs.getString("option_d"));
				},
				attemptId, attempt.quizId());
		return new Result(score, total, total == 0 ? 0 : (int) Math.round(score * 100.0 / total), answers);
	}

	public record Attempt(long id, long quizId, Integer score, Integer total, java.time.OffsetDateTime submittedAt) {}
	public record AnswerResult(
			@JsonProperty("question_id") long questionId,
			@JsonProperty("question_text") String questionText,
			@JsonProperty("selected_option") String selectedOption,
			@JsonProperty("correct_option") String correctOption,
			@JsonProperty("is_correct") boolean isCorrect,
			@JsonProperty("option_a") String optionA,
			@JsonProperty("option_b") String optionB,
			@JsonProperty("option_c") String optionC,
			@JsonProperty("option_d") String optionD) {}
	public record Result(int score, int total, int percentage, List<AnswerResult> answers) {}
}
