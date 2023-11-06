package com.spina.controller;

import com.spina.service.CoinbaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class HomeFinanceController {

    @Autowired
    private CoinbaseService coinbaseService;

    @GetMapping("/btcusdspot")
    public String getBtcUsdSpot() {
        return coinbaseService.getBtcUsdSpot();
    }
    @GetMapping("/btceurspot")
    public String getBtcEurSpot() {
        return coinbaseService.getBtcEurSpot();
    }
}
