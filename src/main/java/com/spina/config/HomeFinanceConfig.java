package com.spina.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class HomeFinanceConfig {
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
