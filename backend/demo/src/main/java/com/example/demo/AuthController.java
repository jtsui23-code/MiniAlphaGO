package com.example.demo;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api")
public class AuthController {

    private final List<User> users = new ArrayList<>();

    @PostMapping("/signup")
    public ResponseEntity<String> signup(@RequestBody SignupRequest request) {
        if (request.getUsername() == null || request.getUsername().isEmpty() ||
            request.getPassword() == null || request.getPassword().isEmpty()) {
            return ResponseEntity.badRequest().body("Invalid signup data");
        }

        // Check if username already exists
        for (User user : users) {
            if (user.getUsername().equals(request.getUsername())) {
                return ResponseEntity.badRequest().body("Username already taken");
            }
        }

        // Add new user
        users.add(new User(request.getUsername(), request.getPassword()));
        return ResponseEntity.ok("User " + request.getUsername() + " registered");
    }

    @PostMapping("/login")
    public ResponseEntity<String> login(@RequestBody LoginRequest request) {
        if (request.getUsername() == null || request.getUsername().isEmpty() ||
            request.getPassword() == null || request.getPassword().isEmpty()) {
            return ResponseEntity.badRequest().body("Invalid login data");
        }

        for (User user : users) {
            if (user.getUsername().equals(request.getUsername()) &&
                user.getPassword().equals(request.getPassword())) {
                return ResponseEntity.ok("Logged in as " + user.getUsername());
            }
        }

        return ResponseEntity.status(401).body("Invalid username or password");
    }
}
