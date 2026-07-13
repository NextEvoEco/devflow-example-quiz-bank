package com.quizbank.quiz;

import java.time.OffsetDateTime;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.quizbank.question.Question;

public record Quiz(
		Long id,
		String name,
		@JsonProperty("question_ids") List<Long> questionIds,
		List<Question> questions,
		@JsonProperty("question_count") Integer questionCount,
		@JsonProperty("created_at") OffsetDateTime createdAt
) {
}
