package com.spina.HomeFinance.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.net.URI;
import java.util.List;

@Service
public class CoinbaseService {
    @Value("${coinbase.url}")
    private String url;
    @Value("${coinbase.readAPIkey}")
    private String apiKey;
    @Value("${coinbase.btcusdpair}")
    private String btcUsdPairEndpoint;
    @Value("${coinbase.btceurpair}")
    private String btcEurPairEndpoint;

    private final RestTemplate restTemplate;
    @Autowired
    public CoinbaseService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public String getBtcUsdSpot() {

        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + apiKey);
        headers.setAccept(List.of(MediaType.APPLICATION_JSON));

        RequestEntity<Void> requestEntity = new RequestEntity<>(headers, HttpMethod.GET, URI.create(btcUsdPairEndpoint));

        ResponseEntity<String> responseEntity = restTemplate.exchange(requestEntity, String.class);

        if (responseEntity.getStatusCodeValue() == 200) {
            System.out.println("BTC/USD Spot Price: " + responseEntity.getBody());
        } else {
            System.out.println("Failed to retrieve data. Status code: " + responseEntity.getStatusCodeValue());
            System.out.println("Response Body: " + responseEntity.getBody());
        }
        return responseEntity.getBody();
    }
    public String getBtcEurSpot() {
        return restTemplate.getForObject(url + btcEurPairEndpoint, String.class);
    }
}
