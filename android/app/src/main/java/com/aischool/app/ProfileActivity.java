package com.aischool.app;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import java.util.ArrayList;
import java.util.List;

public class ProfileActivity extends AppCompatActivity {
    private static final String TAG = "ProfileActivity";
    private static final String PREFS_NAME = "AiSchoolPrefs";
    private static final String TOKEN_KEY = "access_token";

    private TextView tvWelcome;
    private Button btnLogout, btnAddProfile, btnRefresh;
    private RecyclerView rvKidsProfiles;
    private ProfileAdapter profileAdapter;
    private List<KidProfile> kidsProfilesList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        initViews();
        setupRecyclerView();
        setupClickListeners();
        
        loadUserInfo();
        loadKidsProfiles();
    }

    private void initViews() {
        tvWelcome = findViewById(R.id.tvWelcome);
        btnLogout = findViewById(R.id.btnLogout);
        btnAddProfile = findViewById(R.id.btnAddProfile);
        btnRefresh = findViewById(R.id.btnRefresh);
        rvKidsProfiles = findViewById(R.id.rvKidsProfiles);
    }

    private void setupRecyclerView() {
        kidsProfilesList = new ArrayList<>();
        profileAdapter = new ProfileAdapter(kidsProfilesList, this::onProfileClick);
        rvKidsProfiles.setLayoutManager(new LinearLayoutManager(this));
        rvKidsProfiles.setAdapter(profileAdapter);
    }

    private void setupClickListeners() {
        btnLogout.setOnClickListener(v -> performLogout());
        btnAddProfile.setOnClickListener(v -> showCreateProfileDialog());
        btnRefresh.setOnClickListener(v -> loadKidsProfiles());
    }

    private void loadUserInfo() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        String token = prefs.getString(TOKEN_KEY, null);
        
        if (token == null) {
            redirectToLogin();
            return;
        }

        String authorization = "Bearer " + token;
        
        ApiClient.getApiService().getUser(authorization).enqueue(new Callback<ApiResponse>() {
            @Override
            public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    // Display welcome message
                    tvWelcome.setText("Welcome to AI School! 🎓");
                } else {
                    Log.e(TAG, "Failed to load user info: " + response.code());
                    if (response.code() == 401) {
                        clearTokenAndRedirect();
                    }
                }
            }

            @Override
            public void onFailure(Call<ApiResponse> call, Throwable t) {
                Log.e(TAG, "User info error: " + t.getMessage());
                Toast.makeText(ProfileActivity.this, "Connection error", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void loadKidsProfiles() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        String token = prefs.getString(TOKEN_KEY, null);
        
        if (token == null) {
            redirectToLogin();
            return;
        }

        String authorization = "Bearer " + token;
        
        ApiClient.getApiService().getProfiles(authorization).enqueue(new Callback<ApiResponse>() {
            @Override
            public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    List<KidProfile> profiles = response.body().getProfiles();
                    if (profiles != null) {
                        kidsProfilesList.clear();
                        kidsProfilesList.addAll(profiles);
                        profileAdapter.notifyDataSetChanged();
                        
                        Log.d(TAG, "Loaded " + profiles.size() + " kids profiles");
                        Toast.makeText(ProfileActivity.this, "Loaded " + profiles.size() + " profiles", Toast.LENGTH_SHORT).show();
                    } else {
                        Log.d(TAG, "No profiles found");
                        Toast.makeText(ProfileActivity.this, "No kids profiles found. Add one!", Toast.LENGTH_SHORT).show();
                    }
                } else {
                    Log.e(TAG, "Failed to load profiles: " + response.code());
                    Toast.makeText(ProfileActivity.this, "Failed to load profiles", Toast.LENGTH_SHORT).show();
                    
                    if (response.code() == 401) {
                        clearTokenAndRedirect();
                    }
                }
            }

            @Override
            public void onFailure(Call<ApiResponse> call, Throwable t) {
                Log.e(TAG, "Profiles error: " + t.getMessage());
                Toast.makeText(ProfileActivity.this, "Network error: " + t.getMessage(), Toast.LENGTH_LONG).show();
            }
        });
    }

    private void showCreateProfileDialog() {
        // For now, create a sample profile
        // In a real app, you'd show a dialog or new activity for input
        createSampleProfile();
    }

    private void createSampleProfile() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        String token = prefs.getString(TOKEN_KEY, null);
        
        if (token == null) {
            redirectToLogin();
            return;
        }

        // Create a sample kid profile
        KidProfile newProfile = new KidProfile(
            "Sample Kid " + (kidsProfilesList.size() + 1),
            7,
            "2nd Grade",
            "default_avatar",
            "Learning to read and basic math"
        );

        String authorization = "Bearer " + token;
        
        ApiClient.getApiService().createProfile(authorization, newProfile).enqueue(new Callback<ApiResponse>() {
            @Override
            public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Toast.makeText(ProfileActivity.this, "✅ Profile created successfully!", Toast.LENGTH_SHORT).show();
                    loadKidsProfiles(); // Refresh the list
                } else {
                    Log.e(TAG, "Failed to create profile: " + response.code());
                    Toast.makeText(ProfileActivity.this, "❌ Failed to create profile", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<ApiResponse> call, Throwable t) {
                Log.e(TAG, "Create profile error: " + t.getMessage());
                Toast.makeText(ProfileActivity.this, "❌ Network error: " + t.getMessage(), Toast.LENGTH_LONG).show();
            }
        });
    }

    private void onProfileClick(KidProfile profile) {
        Toast.makeText(this, "Selected: " + profile.getName() + " (Age: " + profile.getAge() + ")", Toast.LENGTH_SHORT).show();
        // Here you could navigate to a detailed profile view or learning activity
    }

    private void performLogout() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        String token = prefs.getString(TOKEN_KEY, null);
        
        if (token != null) {
            String authorization = "Bearer " + token;
            
            ApiClient.getApiService().logout(authorization).enqueue(new Callback<ApiResponse>() {
                @Override
                public void onResponse(Call<ApiResponse> call, Response<ApiResponse> response) {
                    clearTokenAndRedirect();
                }

                @Override
                public void onFailure(Call<ApiResponse> call, Throwable t) {
                    Log.e(TAG, "Logout error: " + t.getMessage());
                    clearTokenAndRedirect(); // Still clear token even if logout API fails
                }
            });
        } else {
            clearTokenAndRedirect();
        }
    }

    private void clearTokenAndRedirect() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        prefs.edit().remove(TOKEN_KEY).apply();
        redirectToLogin();
    }

    private void redirectToLogin() {
        Intent intent = new Intent(this, MainActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        startActivity(intent);
        finish();
    }
}
                    clearTokenAndRedirect();
                }
            });
        } else {
            clearTokenAndRedirect();
        }
    }

    private void clearTokenAndRedirect() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        prefs.edit().remove(TOKEN_KEY).apply();
        
        Toast.makeText(this, "Logged out successfully", Toast.LENGTH_SHORT).show();
        
        startActivity(new Intent(this, MainActivity.class));
        finish();
    }
}
