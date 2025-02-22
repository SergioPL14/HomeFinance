package com.spina.HomeFinance.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.function.ServerRequest;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import java.util.List;

@Service
public class CoinbaseService {
    @Value("${coinbase.url}")
    private String url;
    @Value("${coinbase.apiKey}")
    private String apiKey;
    @Value("${coinbase.apiSecret}")
    private String apiSecret;
    @Value("${coinbase.btcusdpair}")
    private String btcUsdPairEndpoint;
    @Value("${coinbase.btceurpair}")
    private String btcEurPairEndpoint;
    @Value("${coinbase.accounts}")
    private String accountsEndpoint;

    private final RestTemplate restTemplate;
    @Autowired
    public CoinbaseService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public String getBtcUsdSpot() {
        HttpHeaders headers = getHeaders();

        RequestEntity<Void> requestEntity = new RequestEntity<>(headers, HttpMethod.GET, URI.create(url + btcUsdPairEndpoint));

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
    public String getAccounts() throws InvalidKeyException, IOException {
        String urlAccounts = url + accountsEndpoint;

        // Paso 1: Obtener el timestamp actual en segundos
        long timestamp = System.currentTimeMillis() / 1000;

        // Paso 2: Definir el método HTTP y la ruta de la solicitud
        String method = "GET";
        String requestPath = "/v2/accounts";

        // Paso 3: Generar la firma
        String signature = generateSignature(apiSecret, timestamp, method, requestPath, "");

        // Paso 4: Hacer la solicitud HTTP
        URL url = new URL(urlAccounts);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod(method);
        connection.setRequestProperty("CB-ACCESS-KEY", apiKey);
        connection.setRequestProperty("CB-ACCESS-SIGN", signature);
        connection.setRequestProperty("CB-ACCESS-TIMESTAMP", String.valueOf(timestamp));
        connection.setRequestProperty("CB-VERSION", "v1.0");

        // Paso 5: Leer la respuesta
        int responseCode = connection.getResponseCode();
        StringBuilder response = new StringBuilder();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();

            System.out.println("Respuesta: " + response.toString());
        } else {
            String errMsg = "Error: " + responseCode;
            System.out.println(errMsg);
            response.append(errMsg);
        }
        return response.toString();
    }

    private HttpHeaders getHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + apiKey);
        headers.setAccept(List.of(MediaType.APPLICATION_JSON));
        return headers;
    }

    private static String generateSignature(String secret, long timestamp, String method, String requestPath, String body) throws InvalidKeyException {
        try {
            // Crear el mensaje para firmar
            String message = timestamp + method + requestPath + body;

            // Crear el objeto HMAC-SHA256
            Mac sha256_HMAC = Mac.getInstance("HmacSHA256");
            SecretKeySpec secretKey = new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
            sha256_HMAC.init(secretKey);

            // Generar la firma y codificarla en Base64
            byte[] hash = sha256_HMAC.doFinal(message.getBytes(StandardCharsets.UTF_8));
            return Base64.getEncoder().encodeToString(hash);
        } catch (NoSuchAlgorithmException | InvalidKeyException e) {
            throw new RuntimeException("Error al generar la firma", e);
        }
    }
}
