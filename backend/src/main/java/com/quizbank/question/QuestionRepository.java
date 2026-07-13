package com.quizbank.question;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Optional;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

@Repository
public class QuestionRepository {

	private static final RowMapper<Question> ROW_MAPPER = QuestionRepository::mapRow;

	private final JdbcTemplate jdbcTemplate;

	public QuestionRepository(JdbcTemplate jdbcTemplate) {
		this.jdbcTemplate = jdbcTemplate;
	}

	public List<Question> findAll() {
		return jdbcTemplate.query(
				"""
				SELECT id, question, option_a, option_b, option_c, option_d,
				       correct, difficulty, created_at, updated_at
				FROM questions
				ORDER BY id ASC
				""",
				ROW_MAPPER);
	}

	public List<Question> search(String query) {
		if (query == null || query.isBlank()) {
			return findAll();
		}
		String pattern = "%" + query.trim().toLowerCase() + "%";
		return jdbcTemplate.query(
				"""
				SELECT id, question, option_a, option_b, option_c, option_d,
				       correct, difficulty, created_at, updated_at
				FROM questions
				WHERE LOWER(question) LIKE ?
				ORDER BY id ASC
				""",
				ROW_MAPPER,
				pattern);
	}

	public Optional<Question> findById(long id) {
		List<Question> rows = jdbcTemplate.query(
				"""
				SELECT id, question, option_a, option_b, option_c, option_d,
				       correct, difficulty, created_at, updated_at
				FROM questions
				WHERE id = ?
				""",
				ROW_MAPPER,
				id);
		return rows.stream().findFirst();
	}

	public Question insert(Question question) {
		Question validated = QuestionValidator.prepare(question);
		KeyHolder keyHolder = new GeneratedKeyHolder();
		jdbcTemplate.update(connection -> {
			var ps = connection.prepareStatement(
					"""
					INSERT INTO questions (
					    question, option_a, option_b, option_c, option_d,
					    correct, difficulty
					) VALUES (?, ?, ?, ?, ?, ?, ?)
					""",
					new String[] {"id"});
			ps.setString(1, validated.question());
			ps.setString(2, validated.optionA());
			ps.setString(3, validated.optionB());
			ps.setString(4, validated.optionC());
			ps.setString(5, validated.optionD());
			ps.setString(6, validated.correct());
			ps.setString(7, validated.difficulty());
			return ps;
		}, keyHolder);

		Number key = keyHolder.getKey();
		if (key == null) {
			throw new IllegalStateException("Failed to obtain generated question id");
		}
		return findById(key.longValue())
				.orElseThrow(() -> new IllegalStateException("Inserted question not found"));
	}

	public Optional<Question> update(long id, Question question) {
		if (findById(id).isEmpty()) {
			return Optional.empty();
		}
		Question validated = QuestionValidator.prepare(question);
		jdbcTemplate.update(
				"""
				UPDATE questions
				SET question = ?,
				    option_a = ?,
				    option_b = ?,
				    option_c = ?,
				    option_d = ?,
				    correct = ?,
				    difficulty = ?,
				    updated_at = NOW()
				WHERE id = ?
				""",
				validated.question(),
				validated.optionA(),
				validated.optionB(),
				validated.optionC(),
				validated.optionD(),
				validated.correct(),
				validated.difficulty(),
				id);
		return findById(id);
	}

	public boolean deleteById(long id) {
		int updated = jdbcTemplate.update("DELETE FROM questions WHERE id = ?", id);
		return updated > 0;
	}

	private static Question mapRow(ResultSet rs, int rowNum) throws SQLException {
		return new Question(
				rs.getLong("id"),
				rs.getString("question"),
				rs.getString("option_a"),
				rs.getString("option_b"),
				rs.getString("option_c"),
				rs.getString("option_d"),
				rs.getString("correct"),
				rs.getString("difficulty"),
				rs.getObject("created_at", java.time.OffsetDateTime.class),
				rs.getObject("updated_at", java.time.OffsetDateTime.class));
	}
}
