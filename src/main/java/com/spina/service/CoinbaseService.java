package com.spina.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class CoinbaseService {
    @Value("${coinbase.url}")
    private String url;
    @Value("${coinbase.btcusdspot}")
    private String btcUsdSpot;
    @Value("${coinbase.btceurspot}")
    private String btcEurSpot;

    private final RestTemplate restTemplate;

    public CoinbaseService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public String getBtcUsdSpot() {
        return restTemplate.getForObject(url + btcUsdSpot, String.class);
    }
    public String getBtcEurSpot() {
        return restTemplate.getForObject(url + btcEurSpot, String.class);
    }
}
