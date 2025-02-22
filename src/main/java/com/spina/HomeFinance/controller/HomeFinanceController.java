package com.spina.HomeFinance.controller;

import com.fasterxml.jackson.databind.introspect.ConcreteBeanPropertyBase;
import com.spina.HomeFinance.service.CoinbaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.net.ProtocolException;
import java.security.InvalidKeyException;

@RestController
@RequestMapping("/api")
public class HomeFinanceController {

    private CoinbaseService coinbaseService;

    @Autowired
    public HomeFinanceController(CoinbaseService coinbaseService) {
        this.coinbaseService = coinbaseService;
    }


    @GetMapping("/btcusdspot")
    public String getBtcUsdSpot() {
        return coinbaseService.getBtcUsdSpot();
    }
    @GetMapping("/btceurspot")
    public String getBtcEurSpot() {
        return coinbaseService.getBtcEurSpot();
    }

    @GetMapping("/accounts")
    public String getAccounts() throws IOException, InvalidKeyException {
        return coinbaseService.getAccounts();
    }
}
