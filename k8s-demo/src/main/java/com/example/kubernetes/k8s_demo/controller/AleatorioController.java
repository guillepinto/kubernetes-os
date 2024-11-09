package com.example.kubernetes.k8s_demo.controller;

import com.example.kubernetes.k8s_demo.servicio.AleatorioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AleatorioController {

    private AleatorioService aleatorioService;

    @GetMapping("/congruencial/lineal/{seed}")
    public Double congruencialLineal(@PathVariable("seed") Long seed) {
        return aleatorioService.congruencialLineal(seed);
    }

    @GetMapping("/congruencial/lineal")
    public Double congruencialLinealWithoutSeed() {
        return aleatorioService.congruencialLineal(null);
    }

    // setter injection
    @Autowired
    public void setAleatorioService(AleatorioService aleatorioService) {
        this.aleatorioService = aleatorioService;
    }
}
