package com.quizbank.web;

import java.nio.file.Path;
import java.nio.file.Paths;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SpaController {

	@Value("${quizbank.frontend.dist:../frontend/dist}")
	private String frontendDist;

	@GetMapping(value = {"/", "/index.html"}, produces = MediaType.TEXT_HTML_VALUE)
	public ResponseEntity<Resource> index() {
		Path index = Paths.get(frontendDist).toAbsolutePath().normalize().resolve("index.html");
		Resource resource = new FileSystemResource(index.toFile());
		if (!resource.exists()) {
			return ResponseEntity.notFound().build();
		}
		return ResponseEntity.ok().contentType(MediaType.TEXT_HTML).body(resource);
	}
}
