package com.example.kubernetes.k8s_demo.servicio;

import org.springframework.stereotype.Service;

@Service
public class AleatorioService {

    private Long m = 2^32L;
    private Long a = 1664525L;
    private Long c = 1013904223L;
    private Long iteraciones = 100000000L;

    public Double congruencialLineal(Long seed) {
        if (seed == null) {
            seed = System.currentTimeMillis();
        }
        Double x = seed.doubleValue();
        for (int i = 0; i < iteraciones; i++) {
            x = (a * x + c) % m;
        }
        return x / m;
    }
}
