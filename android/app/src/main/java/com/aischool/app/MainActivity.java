package com.aischool.app;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";
    private static final String PREFS_NAME = "AiSchoolPrefs";
    private static final String TOKEN_KEY = "access_token";

    private EditText etEmail, etPassword, etFullName, etPhoneNumber;
    private Button btnLogin, btnRegister, btnToggleMode, btnTestConnection;
    private boolean isLoginMode = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initViews();
        setupClickListeners();
        
        // Check if user is already logged in
        checkExistingToken();
        
        // Test server connection
        testServerConnection();
    }

    private void initViews() {
        etEmail = findViewById(R.id.etEmail);
        etPassword = findViewById(R.id.etPassword);
        etFullName = findViewById(R.id.etFullName);
        etPhoneNumber = findViewById(R.id.etPhoneNumber);
        
        btnLogin = findViewById(R.id.btnLogin);
        btnRegister = findViewById(R.id.btnRegister);
        btnToggleMode = findViewById(R.id.btnToggleMode);
        btnTestConnection = findViewById(R.id.btnTestConnection);
        
        updateUIMode();
    }

    private void setupClickListeners() {
        btnLogin.setOnClickListener(v -> performLogin());
        btnRegister.setOnClickListener(v -> performRegister());
        btnToggleMode.setOnClickListener(v -> toggleMode());
        btnTestConnection.setOnClickListener(v -> testServerConnection());
    }

    private void testServerConnection() {
        Log.d(TAG, "Testing server connection...");
        
        ApiClient.getApiService().healthCheck().enqueue(new Callback<ApiResponse>() {
            @Override
            public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                Log.d(TAG, "Health check response: " + response.code());
                if (response.isSuccessful() && response.body() != null) {
                    Toast.makeText(MainActivity.this, "✅ Server connected successfully!", Toast.LENGTH_SHORT).show();
                    Log.d(TAG, "Server health: " + response.body().getMessage());
                } else {
                    Toast.makeText(MainActivity.this, "❌ Server connection failed", Toast.LENGTH_SHORT).show();
                    Log.e(TAG, "Health check failed: " + response.code());
                }
            }

            @Override
            public void onFailure(Call<ApiResponse> call, Throwable t) {
                Log.e(TAG, "Health check error: " + t.getMessage());
                Toast.makeText(MainActivity.this, "❌ Cannot connect to server: " + t.getMessage(), Toast.LENGTH_LONG).show();
            }
        });
    }

    private void toggleMode() {
        isLoginMode = !isLoginMode;
        updateUIMode();
    }

    private void updateUIMode() {
        if (isLoginMode) {
            // Login mode - hide registration fields
            etFullName.setVisibility(View.GONE);
            etPhoneNumber.setVisibility(View.GONE);
            
            btnLogin.setVisibility(View.VISIBLE);
            btnRegister.setVisibility(View.GONE);
            btnToggleMode.setText("Need an account? Register");
        } else {
            // Register mode - show all fields
            etFullName.setVisibility(View.VISIBLE);
            etPhoneNumber.setVisibility(View.VISIBLE);
            
            btnLogin.setVisibility(View.GONE);
            btnRegister.setVisibility(View.VISIBLE);
            btnToggleMode.setText("Have an account? Login");
        }
    }

    private void performLogin() {
        String email = etEmail.getText().toString().trim();
        String password = etPassword.getText().toString().trim();

        if (email.isEmpty() || password.isEmpty()) {
            Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show();
            return;
        }

        User loginUser = new User(email, password);
        
        Log.d(TAG, "Attempting login for: " + email);
        
        ApiClient.getApiService().login(loginUser).enqueue(new Callback<ApiResponse>() {
            @Override
            public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                Log.d(TAG, "Login response code: " + response.code());
                
                if (response.isSuccessful() && response.body() != null) {
                    ApiResponse apiResponse = response.body();
                    String token = apiResponse.getToken();
                    
                    if (token != null && !token.isEmpty()) {
                        // Save token
                        saveToken(token);
                        Toast.makeText(MainActivity.this, "✅ Login successful!", Toast.LENGTH_SHORT).show();
                        
                        // Navigate to ProfileActivity
                        Intent intent = new Intent(MainActivity.this, ProfileActivity.class);
                        startActivity(intent);
                        finish();
                    } else {
                        Toast.makeText(MainActivity.this, "❌ Login failed: No token received", Toast.LENGTH_SHORT).show();
                    }
                } else {
                    try {
                        String errorBody = response.errorBody() != null ? response.errorBody().string() : "Unknown error";
                        Log.e(TAG, "Login failed: " + errorBody);
                        Toast.makeText(MainActivity.this, "❌ Login failed: " + response.code(), Toast.LENGTH_SHORT).show();
                    } catch (Exception e) {
                        Log.e(TAG, "Error reading error body", e);
                        Toast.makeText(MainActivity.this, "❌ Login failed", Toast.LENGTH_SHORT).show();
                    }
                }
            }

            @Override
            public void onFailure(Call<ApiResponse> call, Throwable t) {
                Log.e(TAG, "Login network error: " + t.getMessage());
                Toast.makeText(MainActivity.this, "❌ Network error: " + t.getMessage(), Toast.LENGTH_LONG).show();
            }
        });
    }
    private void performRegister() {
        String email = etEmail.getText().toString().trim();
        String password = etPassword.getText().toString().trim();
        String fullName = etFullName.getText().toString().trim();
        String phoneNumber = etPhoneNumber.getText().toString().trim();

        if (email.isEmpty() || password.isEmpty() || fullName.isEmpty() || phoneNumber.isEmpty()) {
            Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show();
            return;
        }

        User registerUser = new User(email, password, fullName, phoneNumber);
        
        Log.d(TAG, "Attempting registration for: " + email);
        
        ApiClient.getApiService().register(registerUser).enqueue(new Callback<ApiResponse>() {
            @Override
            public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                Log.d(TAG, "Registration response code: " + response.code());
                
                if (response.isSuccessful() && response.body() != null) {
                    ApiResponse apiResponse = response.body();
                    String token = apiResponse.getToken();
                    
                    if (token != null && !token.isEmpty()) {
                        // Save token
                        saveToken(token);
                        Toast.makeText(MainActivity.this, "✅ Registration successful!", Toast.LENGTH_SHORT).show();
                        
                        // Navigate to ProfileActivity
                        Intent intent = new Intent(MainActivity.this, ProfileActivity.class);
                        startActivity(intent);
                        finish();
                    } else {
                        Toast.makeText(MainActivity.this, "❌ Registration failed: No token received", Toast.LENGTH_SHORT).show();
                    }
                } else {
                    try {
                        String errorBody = response.errorBody() != null ? response.errorBody().string() : "Unknown error";
                        Log.e(TAG, "Registration failed: " + errorBody);
                        
                        if (response.code() == 409) {
                            Toast.makeText(MainActivity.this, "❌ User already exists. Try logging in.", Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(MainActivity.this, "❌ Registration failed: " + response.code(), Toast.LENGTH_SHORT).show();
                        }
                    } catch (Exception e) {
                        Log.e(TAG, "Error reading error body", e);
                        Toast.makeText(MainActivity.this, "❌ Registration failed", Toast.LENGTH_SHORT).show();
                    }
                }
            }

            @Override
            public void onFailure(Call<ApiResponse> call, Throwable t) {
                Log.e(TAG, "Registration network error: " + t.getMessage());
                Toast.makeText(MainActivity.this, "❌ Network error: " + t.getMessage(), Toast.LENGTH_LONG).show();
            }
        });
    }

    private void checkExistingToken() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        String token = prefs.getString(TOKEN_KEY, null);
        
        if (token != null && !token.isEmpty()) {
            // Token exists, verify it's still valid
            ApiClient.getApiService().getUser("Bearer " + token).enqueue(new Callback<ApiResponse>() {
                @Override
                public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                    if (response.isSuccessful()) {
                        // Token is valid, go to profile
                        startActivity(new Intent(MainActivity.this, ProfileActivity.class));
                        finish();
                    } else {
                        // Token invalid, clear it
                        clearToken();
                    }
                }

                @Override
                public void onFailure(Call<ApiResponse> call, Throwable t) {
                    // Network error, assume token is still valid
                    Log.e(TAG, "Token validation failed: " + t.getMessage());
                }
            });
        }
    }

    private void saveToken(String token) {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        prefs.edit().putString(TOKEN_KEY, token).apply();
        Log.d(TAG, "Token saved successfully");
    }
    
    private void clearToken() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        prefs.edit().remove(TOKEN_KEY).apply();
        Log.d(TAG, "Token cleared");
    }
}
            public void onFailure(Call<ApiResponse> call, Throwable t) {
                Log.e(TAG, "Login error: " + t.getMessage());
                Toast.makeText(MainActivity.this, "Login error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void performRegister() {
        String username = etUsername.getText().toString().trim();
        String password = etPassword.getText().toString().trim();
        String email = etEmail.getText().toString().trim();
        String fullName = etFullName.getText().toString().trim();
        String dob = etDob.getText().toString().trim();
        String location = etLocation.getText().toString().trim();

        if (username.isEmpty() || password.isEmpty() || email.isEmpty() || 
            fullName.isEmpty() || dob.isEmpty() || location.isEmpty()) {
            Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show();
            return;
        }

        User registerUser = new User(username, password, email, fullName, dob, location);
        
        ApiClient.getApiService().register(registerUser).enqueue(new Callback<ApiResponse>() {
            @Override
            public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Toast.makeText(MainActivity.this, "Registration successful! Please login.", Toast.LENGTH_SHORT).show();
                    
                    // Switch to login mode
                    isLoginMode = true;
                    updateUIMode();
                } else {
                    Toast.makeText(MainActivity.this, "Registration failed: User may already exist", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<ApiResponse> call, Throwable t) {
                Log.e(TAG, "Registration error: " + t.getMessage());
                Toast.makeText(MainActivity.this, "Registration error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void saveToken(String token) {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        prefs.edit().putString(TOKEN_KEY, token).apply();
    }

    private void checkExistingToken() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        String token = prefs.getString(TOKEN_KEY, null);
        
        if (token != null) {
            // User already logged in, go to profile
            startActivity(new Intent(this, ProfileActivity.class));
            finish();
        }
    }
}
