package com.quizbank.config;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.web.servlet.resource.PathResourceResolver;

@Configuration
public class WebConfig implements WebMvcConfigurer {

	@Value("${quizbank.frontend.dist:../frontend/dist}")
	private String frontendDist;

	@Override
	public void addResourceHandlers(ResourceHandlerRegistry registry) {
		Path distPath = Paths.get(frontendDist).toAbsolutePath().normalize();
		String location = distPath.toUri().toString();
		if (!location.endsWith("/")) {
			location = location + "/";
		}

		registry.setOrder(0);
		registry.addResourceHandler("/**")
				.addResourceLocations(location)
				.resourceChain(true)
				.addResolver(new PathResourceResolver() {
					@Override
					protected Resource getResource(String resourcePath, Resource location) throws java.io.IOException {
						if (resourcePath != null && resourcePath.startsWith("api/")) {
							return null;
						}
						Resource requested = super.getResource(resourcePath, location);
						if (requested != null) {
							return requested;
						}
						Path index = distPath.resolve("index.html");
						if (Files.isRegularFile(index)) {
							return new FileSystemResource(index.toFile());
						}
						return null;
					}
				});
	}
}
