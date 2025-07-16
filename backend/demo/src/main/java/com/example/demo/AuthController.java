package com.example.demo;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class AuthController {

    @PostMapping("/login")
    public ResponseEntity<String> login(@RequestBody LoginRequest request) {
        if (request.getUsername() != null && !request.getUsername().isEmpty() &&
            request.getPassword() != null && !request.getPassword().isEmpty()) {
            return ResponseEntity.ok("Logged in as " + request.getUsername());
        }
        return ResponseEntity.badRequest().body("Invalid login data");
    }

    @PostMapping("/signup")
    public ResponseEntity<String> signup(@RequestBody SignupRequest request) {
        if (request.getUsername() != null && !request.getUsername().isEmpty() &&
            request.getPassword() != null && !request.getPassword().isEmpty()) {
            return ResponseEntity.ok("User " + request.getUsername() + " registered");
        }
        return ResponseEntity.badRequest().body("Invalid signup data");
    }
}
