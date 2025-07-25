package com.geosight.backend.config;

import io.github.cdimascio.dotenv.Dotenv;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.boot.jdbc.DataSourceBuilder;

import javax.sql.DataSource;

@Configuration
public class DatabaseConfig {

    @Bean
    public DataSource dataSource() {
        Dotenv dotenv = Dotenv.configure()
                              .directory("./backend") // Adjust path if needed
                              .ignoreIfMalformed()
                              .ignoreIfMissing()
                              .load();

        return DataSourceBuilder.create()
                .url(dotenv.get("DB_URL"))
                .username(dotenv.get("DB_USERNAME"))
                .password(dotenv.get("DB_PASSWORD"))
                .build();
    }
}

